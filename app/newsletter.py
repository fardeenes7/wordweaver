from django.core.mail import EmailMessage
from django.template.loader import render_to_string
from django.core.mail import EmailMultiAlternatives
from django.utils import timezone
from blog.models import Post
from datetime import timedelta
from django.utils.html import strip_tags
from django.conf import settings
from django.db.models import Count, F


def get_most_viewed_posts():
    # Calculate the date 30 days ago from today
    thirty_days_ago = timezone.now() - timedelta(days=30)

    # Filter posts that have at least one view in the last 30 days
    posts = Post.objects.filter(view__date__gte=thirty_days_ago)

    # Annotate each post with the view count in the last 30 days
    # posts = posts.annotate(views_in_last_30_days=Count('view', filter=F('view__date__gte', thirty_days_ago)))
    # posts = posts.annotate(views_in_last_30_days=Count('view', filter=F('view__date__gte', thirty_days_ago)))
    posts = posts.annotate(views_in_last_30_days=Count('view'))

    posts = posts.filter(view__date__gte=thirty_days_ago)

    # Order the posts by views in the last 30 days in descending order
    posts = posts.order_by('-views_in_last_30_days')[:5]
    print(posts)

    return posts
    
from user.models import Subscriber
def newsletter_email():
    # Create a dictionary with the data to pass to the email template
    month = timezone.now().strftime('%B %Y')
    
    # filter the posts that have the most views in the last 30 days
    posts = get_most_viewed_posts()
    
    data = {
        'base_url': 'http://127.0.0.1:8000/',  # Note: Use http:// in the URL
        'message': f'Newsletter for {month}',
        'title': f'Newsletter for {month}',
        'posts': posts,  # Use the filtered 'posts'
    }
    
    # Render the HTML email content from a template
    html_message = render_to_string('email/newsletter.html', data)
   
    # Create a plain text version for the email (optional)
    text_message = strip_tags(html_message)
    
    recipient_list = [user.email for user in Subscriber.objects.all()]
    
    # Create the EmailMessage and send it
    # email = EmailMessage(data['message'], html_message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    email  = EmailMultiAlternatives(data['message'], text_message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    email.attach_alternative(html_message, "text/html")
    
    email.send(fail_silently=False)
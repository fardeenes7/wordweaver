from django.core.mail import EmailMultiAlternatives
from django.template.loader import render_to_string
from django.utils.html import strip_tags
from django.conf import settings
from django.contrib.auth.models import User


def new_article_email(article):
    # Create a dictionary with the data to pass to the email template
    data = {
        'image': f'http://127.0.0.1:8000/media/{article.image}',
        'message': 'A new article has been published.',
        'title': article.title,
        'excerpt': article.excerpt,
        'url': f'http://127.0.0.1:8000/blog/{article.slug}',
        'action': 'Read More',
        'note': ''
    }

    # Render the HTML email content from a template
    html_message = render_to_string('email/single_post.html', data)

    # Create a plain text version for the email (optional)
    text_message = strip_tags(html_message)
    recipient_list = []
    for user in User.objects.filter(new_post_email=True):
        recipient_list.append(user.email)

    # Create the EmailMessage and send it
    email  = EmailMultiAlternatives(data['message'], text_message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    email.attach_alternative(html_message, "text/html")
    
    email.send(fail_silently=False)


def email_publish_notification(article):
    # Create a dictionary with the data to pass to the email template
    data = {
        'image': f'http://127.0.0.1:8000/media/{article.image}',
        'message': 'Your article is live now.',
        'title': article.title,
        'excerpt': article.excerpt,
        'url': f'http://127.0.0.1:8000/blog/{article.slug}',
        'action': 'View Article',
        'note':''
    }

    # Render the HTML email content from a template
    html_message = render_to_string('email/single_post.html', data)

    # Create a plain text version for the email (optional)
    text_message = strip_tags(html_message)
    recipient_list = [article.author.email]

    # Create the EmailMessage and send it
    email  = EmailMultiAlternatives(data['message'], text_message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    email.attach_alternative(html_message, "text/html")
    
    email.send(fail_silently=False)


def email_flagged_notification(article):
    # Create a dictionary with the data to pass to the email template
    data = {
        'image': f'http://127.0.0.1:8000/media/{article.image}',
        'message': 'Your article is flagged for offensive words.',
        'title': article.title,
        'excerpt': article.excerpt,
        'url': f'http://127.0.0.1:8000/user/post/{article.slug}',
        'action': 'Edit Post',
        'note': f'Blocked for using these words: {article.flag_comment}'
    }

    # Render the HTML email content from a template
    html_message = render_to_string('email/single_post.html', data)

    # Create a plain text version for the email (optional)
    text_message = strip_tags(html_message)
    recipient_list = [article.author.email]

    # Create the EmailMessage and send it
    email  = EmailMultiAlternatives(data['message'], text_message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    email.attach_alternative(html_message, "text/html")
    
    email.send(fail_silently=False)

def email_rejection_notification(article):
    # Create a dictionary with the data to pass to the email template
    data = {
        'image': f'http://127.0.0.1:8000/media/{article.image}',
        'message': 'Your article is rejected by admins.',
        'title': article.title,
        'excerpt': article.excerpt,
        'url': f'http://127.0.0.1:8000/user/post/{article.slug}',
        'action': 'Edit Post',
        'note': f'Admin Comment: {article.admin_comment}'
    }

    # Render the HTML email content from a template
    html_message = render_to_string('email/single_post.html', data)

    # Create a plain text version for the email (optional)
    text_message = strip_tags(html_message)
    recipient_list = [article.author.email]

    # Create the EmailMessage and send it
    email  = EmailMultiAlternatives(data['message'], text_message, settings.DEFAULT_FROM_EMAIL, recipient_list)
    email.attach_alternative(html_message, "text/html")
    
    email.send(fail_silently=False)



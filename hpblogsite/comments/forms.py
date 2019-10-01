# -*- coding: UTF-8 -*-
# by Hp

from django import forms
from .models import Comment


class CommentForm(forms.ModelForm):
    class Meta:
        model = Comment
        fields = ['name', 'email', 'url', 'text']
        
        widgets = {
            "name": forms.widgets.TextInput(attrs={"placeholder": "Name",
                                                   "type": "text",
                                                   "name": "demo-name",
                                                   "id": "demo-name"
                                                   }),
            "email": forms.widgets.TextInput(attrs={"placeholder": "Email",
                                                    "type": "email",
                                                    "name": "demo-email",
                                                    "id": "demo-email"
                                                    }),
            "text": forms.widgets.Textarea(attrs={"placeholder": "Enter your message",
                                                  "type": "text",
                                                  "name": "demo-message",
                                                  "id": "demo-message"
                                                  }),
        }

from .models import User, Auction, Bid, Comment
from django.forms import ModelForm
from django.forms.widgets import NumberInput, Select, TextInput


class AuctionForm(ModelForm):
    class Meta:
        model = Auction
        fields = [
            'title',
            'image',
            'image_url',
            'category',
            'description',
            'starting_bid',
        ]


class BidForm(ModelForm):
    class Meta:
        model = Bid
        labels = {
            'bid_amount': ''
        }
        widgets = {
            'bid_amount': NumberInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Bid Amount'
                }
            ),
        }
        fields = ['bid_amount']


class CommentForm(ModelForm):
    class Meta:
        model = Comment
        labels = {
            'comment': ''
        }
        widgets = {
            'comment': TextInput(
                attrs={
                    'class': 'form-control',
                    'placeholder': 'Add Comment...'
                }
            ),
        }
        fields = ['comment']

from django import forms
from .models import Ticket, TicketMessage

class TicketCreateForm(forms.ModelForm):
    description = forms.CharField(
        widget=forms.Textarea(attrs={'rows': 5}),
        help_text='Initial message for the ticket',
        required=True
    )
    attachment = forms.FileField(
        required=False,
        help_text='Attach a file to your message'
    )

    class Meta:
        model = Ticket
        fields = ['title']

    def save(self, commit=True):
        ticket = super().save(commit=False)
        if commit:
            ticket.save()
            # Create the initial ticket message with attachment
            TicketMessage.objects.create(
                ticket=ticket,
                user=self.instance.created_by,
                content=self.cleaned_data['description'],
                attachment=self.cleaned_data.get('attachment')
            )
        return ticket

class TicketMessageForm(forms.ModelForm):
    class Meta:
        model = TicketMessage
        fields = ['content', 'attachment']
        widgets = {
            'content': forms.Textarea(attrs={'rows': 5}),
        }

    def __init__(self, *args, **kwargs):
        self.user = kwargs.pop('user', None)
        self.ticket = kwargs.pop('ticket', None)
        self.replied_to = kwargs.pop('replied_to', None)
        super().__init__(*args, **kwargs)

    def save(self, commit=True):
        message = super().save(commit=False)
        message.user = self.user
        message.ticket = self.ticket
        message.replied_to = self.replied_to
        if commit:
            message.save()
        return message
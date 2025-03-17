from django.shortcuts import render, get_object_or_404, redirect
from django.views.generic import ListView, DetailView, CreateView, UpdateView
from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.urls import reverse_lazy
from django.http import HttpResponseForbidden

from .forms import TicketCreateForm, TicketMessageForm
from .models import Ticket, TicketMessage
from django.contrib.auth.decorators import login_required, permission_required
from django.contrib import messages
from .mixins import TicketAccessMixin
from django.core.exceptions import PermissionDenied

class TicketListView(LoginRequiredMixin, ListView):
    model = Ticket
    template_name = 'tickets/ticket_list.html'
    context_object_name = 'tickets'
    paginate_by = 10

    def get_queryset(self):
        if self.request.user.has_perm('tickets.can_view_all_tickets'):
            return Ticket.objects.all()
        return Ticket.objects.filter(created_by=self.request.user)

class TicketDetailView(LoginRequiredMixin, TicketAccessMixin, DetailView):
    model = Ticket
    template_name = 'tickets/ticket_detail.html'
    context_object_name = 'ticket'

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['form'] = TicketMessageForm()
        context['replies'] = self.object.messages.all().order_by('created_at')
        return context

@login_required
def ticket_reply(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if ticket.status == 'closed':
        messages.error(request, 'Cannot reply to a closed ticket!')
        return redirect('ticket-detail', pk=pk)
    if request.method == 'POST':
        last_message = ticket.messages.last()
        form = TicketMessageForm(request.POST, request.FILES, user=request.user, ticket=ticket, replied_to=last_message)
        if form.is_valid():
            form.save()
            messages.success(request, 'Reply added successfully!')
            return redirect('ticket-detail', pk=pk)
    return redirect('ticket-detail', pk=pk)

class TicketCreateView(LoginRequiredMixin, CreateView):
    form_class = TicketCreateForm
    template_name = 'tickets/ticket_form.html'
    success_url = reverse_lazy('ticket-list')

    def dispatch(self, request, *args, **kwargs):
        if request.user.has_perm('tickets.can_create_ticket'):
            messages.error(request, 'Managers cannot create tickets.')
            return redirect('ticket-list')
        return super().dispatch(request, *args, **kwargs)

    def form_valid(self, form):
        form.instance.created_by = self.request.user
        form.instance.status = 'open'
        messages.success(self.request, 'Ticket created successfully!')
        return super().form_valid(form)

@login_required
def close_ticket(request, pk):
    ticket = get_object_or_404(Ticket, pk=pk)
    if request.method == 'POST':
        if request.user == ticket.created_by or request.user.has_perm('tickets.can_view_all_tickets'):
            ticket.status = 'closed'
            ticket.save()
            messages.success(request, 'Ticket closed successfully!')
            return redirect('ticket-detail', pk=pk)
        return HttpResponseForbidden()
    return redirect('ticket-detail', pk=pk)

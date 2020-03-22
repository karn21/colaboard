from django.shortcuts import render, redirect
from django.views.generic import View, UpdateView
from .forms import BoardCreationForm
from django.contrib import messages
from .models import Board, BoardList, ListCard
from .forms import ListModelFormset, CardCreationForm
from django.contrib.auth.models import User
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.template.loader import render_to_string
from django.core.mail import send_mail


@login_required
def dashboard(request):
    user = request.user
    boards = Board.objects.filter(creator=user)
    team_boards = Board.objects.filter(team=user)
    context = {
        'boards': boards,
        'team_boards': team_boards
    }
    return render(request, 'dashboard.html', context)


def add_users(request, invite_users, board):
    for user in invite_users:
        if user == request.user.email:
            continue
        if User.objects.filter(email=user).exists():
            user = User.objects.get(email=user)
            subject = 'You have been invited to a board.'
            message = render_to_string('board_invitation.html', {
                'user': user,
                'by_user': request.user,
                'board': board,
                'domain': request.META['HTTP_HOST'],
            })
            user.email_user(subject, message)
            board.team.add(user)
        else:
            domain = request.META['HTTP_HOST']
            url = redirect('boards:board_join', slug=board.slug)
            subject = 'You have been invited to a board.'
            body = f'You have been invited to work on a board.Go ahead and check it out. http://{ domain }{url.url}'
            send_mail(subject, body,
                      '2018ucp1323@mnit.ac.in', [user])
    messages.info(request, 'Your invitation has been sent to your team.')
    board.save()


class BoardCreateView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        form = BoardCreationForm()
        context = {
            'form': form
        }
        return render(self.request, 'create_board.html', context)

    def post(self, *args, **kwargs):
        form = BoardCreationForm(self.request.POST or None)
        if form.is_valid():
            board = form.save(commit=False)
            board.creator = self.request.user
            board.save()
            if board.board_type == 'T':
                invite = self.request.POST.get('invite')
                invite_users = invite.split(',')
                add_users(self.request, invite_users, board)
            messages.info(
                self.request, 'Your new Board has been created. Go ahead and add lists..')
            return redirect('boards:board_detail', slug=board.slug)
        else:
            return redirect(".")


@login_required
def board_detail(request, slug):
    board = Board.objects.get(slug=slug)
    form = CardCreationForm()
    domain = request.get_host(),
    url = redirect('boards:board_join', slug=board.slug)
    invite_link = f'http://{ domain[0] }{url.url}'
    context = {
        'board': board,
        'form': form,
        'invite_link': invite_link
    }
    return render(request, 'board_detail.html', context)


@login_required
def board_edit(request):
    if request.method == "POST":
        board_id = request.POST.get('board-id')
        board = Board.objects.get(pk=board_id)
        new_title = request.POST.get('new-title')
        board.title = new_title
        board.save()
        messages.success(request, 'Board has been updated.')
        return redirect('boards:dashboard')
    else:
        return redirect('boards:dashboard')


@login_required
def board_delete(request):
    if request.method == 'POST':
        board_id = request.POST.get('board-id')
        board = Board.objects.get(pk=board_id)
        if board.creator == request.user:
            board.delete()
            messages.warning(request, 'Board deleted successfully.')
        else:
            messages.warning(
                request, 'This is a Team Board. Only the creator can delete.')
        return redirect('boards:dashboard')
    else:
        return redirect('boards:dashboard')


@login_required
def board_join(request, slug):
    user = request.user
    board = Board.objects.get(slug=slug)
    board.team.add(user)
    board.save()
    messages.info(
        request, f'You have joined the Board {board.title} successfully')
    return redirect('boards:dashboard')


def board_invite(request, slug):
    invite = request.POST.get('invite')
    invite_users = invite.split(',')
    board = Board.objects.get(slug=slug)
    board.board_type = 'T'
    board.save()
    add_users(request, invite_users, board)
    return redirect('boards:board_detail', slug=slug)


@login_required
def create_list(request, board_slug):
    if request.method == 'GET':
        formset = ListModelFormset(queryset=BoardList.objects.none())
    elif request.method == 'POST':
        formset = ListModelFormset(request.POST)
        board = Board.objects.get(creator=request.user, slug=board_slug)
        if formset.is_valid():
            for form in formset:
                if form.cleaned_data.get('title'):
                    board_list = form.save(commit=False)
                    board_list.board = board
                    board_list.save()
            messages.success(
                request, 'Your List has been created successfully. Go ahead and add some cards!')
            return redirect('boards:board_detail', slug=board_slug)
    return render(request, 'create_list.html', {'formset': formset, })


@login_required
def list_edit(request):
    if request.method == "POST":
        list_id = request.POST.get('list-id')
        board_list = BoardList.objects.get(pk=list_id)
        new_title = request.POST.get('new-title')
        board_list.title = new_title
        board_list.save()
        messages.success(request, 'List has been updated.')
        return redirect('boards:board_detail', slug=board_list.board.slug)
    else:
        return redirect('boards:board_detail', slug=board_list.board.slug)


@login_required
def list_delete(request):
    if request.method == 'POST':
        list_id = request.POST.get('list-id')
        board = BoardList.objects.get(pk=list_id).board
        if board.creator == request.user:
            BoardList.objects.filter(pk=list_id).delete()
            messages.warning(request, 'List deleted successfully.')
        else:
            messages.warning(
                request, 'This is a Team Board. Only the creator can delete.')
        return redirect('boards:board_detail', slug=board.slug)
    else:
        return redirect('boards:board_detail', slug=board.slug)


class CardCreateView(LoginRequiredMixin, View):
    def get(self, *args, **kwargs):
        return render(self.request, 'create_card.html')

    def post(self, *args, **kwargs):
        list_id = self.request.POST.get('list-id')
        form = CardCreationForm(self.request.POST or None, self.request.FILES)
        board_list = BoardList.objects.get(pk=list_id)
        if form.is_valid():
            card = form.save(commit=False)
            card.board_list = board_list
            card.save()
            messages.success(self.request, 'Card added successfully.')
            return redirect("boards:board_detail", slug=board_list.board.slug)
        else:
            messages.warning(self.request, 'Some Error occured')
            return redirect("boards:board_detail", slug=board_list.board.slug)


class CardUpdateView(LoginRequiredMixin, UpdateView):
    model = ListCard
    form_class = CardCreationForm
    template_name = 'edit_card.html'
    pk_url_kwarg = 'card_pk'
    context_object_name = 'card'

    def form_valid(self, form):
        card = form.save()
        board = card.board_list.board
        messages.success(self.request, 'Card has been updated.')
        return redirect('boards:board_detail', slug=board.slug)


@login_required
def card_delete(request):
    if request.method == 'POST':
        card_id = request.POST.get('card-id')
        board = ListCard.objects.get(pk=card_id).board_list.board
        if board.creator == request.user:
            ListCard.objects.filter(pk=card_id).delete()
            messages.warning(request, 'Card deleted successfully.')
        else:
            messages.warning(
                request, 'This is a Team Board. Only the creator can delete')
        return redirect('boards:board_detail', slug=board.slug)
    else:
        return redirect('boards:board_detail', slug=board.slug)


@login_required
def card_archive(request, card_pk):
    card = ListCard.objects.get(pk=card_pk)
    if card.archived == True:
        card.archived = False
        messages.success(request, 'Card Unarchived.')
    else:
        card.archived = True
        messages.success(request, 'Card moved to Archive.')
    card.save()
    return redirect('boards:board_detail', card.board_list.board.slug)


@login_required
def card_check(request, card_pk):
    card = ListCard.objects.get(pk=card_pk)
    if card.checked == True:
        card.checked = False
        messages.success(request, 'Card Unchecked.')
    else:
        card.checked = True
        messages.success(request, 'Card Checked.')
    card.save()
    return redirect('boards:board_detail', card.board_list.board.slug)


@login_required
def card_move(request, card_pk):
    if request.method == "POST":
        card = ListCard.objects.get(pk=card_pk)
        list_id = request.POST.get('new_list')
        new_list = BoardList.objects.get(pk=list_id)
        card.board_list = new_list
        card.save()
        messages.success(request, 'Your Card has been moved.')
        return redirect('boards:board_detail', card.board_list.board.slug)
    else:
        card = ListCard.objects.get(pk=card_pk)
        board = card.board_list.board
        board_lists = board.board_list.all()
        context = {
            'board_lists': board_lists
        }
        return render(request, 'move_card.html', context)

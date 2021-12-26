import random
from markdown2 import Markdown
from django.shortcuts import render
from django.http import HttpResponse, HttpResponseRedirect
from django.urls import reverse
from django import forms as frm
from . import util, forms




def index(request):
    return render(request, "encyclopedia/index.html", {
        "entries": util.list_entries()
    })


def entry_page(request, entry):
    mrk = Markdown()
    entrypage= util.get_entry(entry)

    if entrypage is None:
        return render(request, 'encyclopedia/nonexistingentry.html', {"entrytitle": entry})
    else:
        context = {
            "entry": mrk.convert(entrypage),
            "entrytitle": entry
        }
        return render(request, "encyclopedia/entrypage.html", context)


def search(request):
    query = request.GET.get('q', '')
    search_entry = util.get_entry(query)
    list_entries = util.list_entries()

    if search_entry is not None:
        return HttpResponseRedirect(reverse('entry_page', kwargs={'entry': query}))
    else:
        substring = []
        for entry in list_entries:
            if query.lower() in entry.lower():
                substring.append(entry)

        context = {
            "entries": substring,
            "search": True,
            "query": query
        }
        return render(request, "encyclopedia/index.html", context)


def new_entry(request):
    if request.method == "POST":
        form = forms.NewEntryForm(request.POST)
        if form.is_valid():
            title = form.cleaned_data['title']
            content = form.cleaned_data['content']
            get_entry = util.get_entry(title)

            if get_entry is None or form.cleaned_data["edit"] is True:
                util.save_entry(title, content)
                return HttpResponseRedirect(reverse("entry_page", kwargs={'entry': title}))
            else:
                context = {
                    'form': form,
                    'exist': True,
                    'entry': title
                }
                return render(request, "encyclopedia/newentry.html", context)
        else:
            context = {
                'form': form,
                'exist': False
            }
            return render(request, "encyclopedia/newentry.html", context)
    else:
        context = {
            'form': forms.NewEntryForm(),
            'existing': False
        }

        return render(request, "encyclopedia/newentry.html", context)


def edit_page(request, entry):
    get_entry = util.get_entry(entry)
    if get_entry is None:
        return render(request, "encyclopedia/nonexistingentry.html", {"entrytitle": entry})
    else:
        form = forms.NewEntryForm()
        form.fields["title"].initial = entry
        form.fields["title"].widget = frm.HiddenInput()
        form.fields["content"].initial = get_entry
        form.fields["edit"].initial = True

        context = {
            "form": form,
            "title": form.fields["title"].initial,
            "edit": form.fields["edit"].initial
        }

        return render(request, "encyclopedia/newentry.html", context)



def random_page(request):
    entries = util.list_entries()
    random_entry = random.choice(entries)

    return HttpResponseRedirect(reverse("entry_page", kwargs={"entry": random_entry}))









from django.contrib.admin.views.decorators import staff_member_required
from django.shortcuts import render_to_response
from django.template.context import RequestContext
from reviewboard.extensionbrowser.base import ExtensionStoreQuery
from reviewboard.extensionbrowser.forms import SearchForm
from reviewboard.extensions.base import get_extension_manager


@staff_member_required
def browse_extensions(request,
                      template_name='extensionbrowser/extension_browser.html'):
    """Main view for the extension browser module."""
    results = None

    if request.method == 'POST':
        form = SearchForm(request.POST)

        if form.is_valid():
            store = ExtensionStoreQuery(get_extension_manager())
            results = store.populate_extensions(request.POST)

    else:
        form = SearchForm()

    return render_to_response(template_name, RequestContext(request, {
        'results': results,
        'form': form
    }))
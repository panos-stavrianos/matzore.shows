# coding=utf-8

from google.cloud import storage
from wtforms import Field, widgets
from wtforms.widgets import HTMLString

from app import app

cdn = [
    [
        'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-treeview/1.2.0/bootstrap-treeview.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.3.1/css/bootstrap.css',
        'https://cdn.datatables.net/1.10.20/css/dataTables.bootstrap4.min.css',
        'https://cdn.datatables.net/responsive/2.2.3/css/responsive.bootstrap4.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/font-awesome/5.11.2/css/all.min.css',
        'https://fonts.googleapis.com/css?family=Nunito:200,200i,300,300i,400,400i,600,600i,700,700i,800,800i,900,900i',
        'https://cdnjs.cloudflare.com/ajax/libs/ion-rangeslider/2.3.0/css/ion.rangeSlider.min.css',
        'https://cdnjs.cloudflare.com/ajax/libs/jquery.inputmask/3.3.4/css/inputmask.min.css',
        'https://cdn.datatables.net/responsive/2.2.3/css/responsive.dataTables.min.css',
        'https://cdn.jsdelivr.net/gh/gitbrent/bootstrap4-toggle@3.6.1/css/bootstrap4-toggle.min.css',
        "https://cdnjs.cloudflare.com/ajax/libs/codemirror/5.48.4/codemirror.css",
        "https://cdnjs.cloudflare.com/ajax/libs/highlight.js/9.12.0/styles/github.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/tui-editor/1.4.10/tui-editor-contents.min.css",
        "https://cdnjs.cloudflare.com/ajax/libs/tui-editor/1.4.10/tui-editor.min.css",
        'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-select/1.13.11/css/bootstrap-select.min.css',
        'https://cdn.jsdelivr.net/npm/select2@4.0.13/dist/css/select2.min.css',
        'https://unpkg.com/gijgo@1.9.13/css/gijgo.min.css'
    ], [
        'https://code.jquery.com/jquery-3.4.1.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/bootstrap-treeview/1.2.0/bootstrap-treeview.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/twitter-bootstrap/4.3.1/js/bootstrap.bundle.min.js',
        'https://cdn.datatables.net/1.10.20/js/jquery.dataTables.min.js',
        'https://cdn.datatables.net/1.10.20/js/dataTables.bootstrap4.min.js',
        'https://cdn.datatables.net/responsive/2.2.3/js/dataTables.responsive.min.js',
        'https://cdn.datatables.net/responsive/2.2.3/js/responsive.bootstrap4.min.js',
        'https://cdn.datatables.net/scroller/2.0.1/js/dataTables.scroller.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/jquery.inputmask/3.3.4/inputmask/inputmask.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.24.0/moment.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/ion-rangeslider/2.3.0/js/ion.rangeSlider.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/moment.js/2.24.0/moment-with-locales.min.js',
        'https://cdnjs.cloudflare.com/ajax/libs/jquery-easing/1.4.1/jquery.easing.min.js',
        "https://www.gstatic.com/firebasejs/7.5.0/firebase-app.js",
        "https://www.gstatic.com/firebasejs/7.5.0/firebase-analytics.js",
        'https://www.gstatic.com/firebasejs/7.5.0/firebase-messaging.js',
        'https://unpkg.com/popper.js',
        'https://cdn.jsdelivr.net/gh/gitbrent/bootstrap4-toggle@3.6.1/js/bootstrap4-toggle.min.js',
        "https://code.highcharts.com/highcharts.js",
        "https://code.highcharts.com/highcharts-more.js",
        "https://code.highcharts.com/modules/solid-gauge.js",
        'https://cdnjs.cloudflare.com/ajax/libs/socket.io/2.2.0/socket.io.js',
        'https://cdnjs.cloudflare.com/ajax/libs/tui-editor/1.4.10/tui-editor-Editor-full.min.js',
        'https://cdn.jsdelivr.net/npm/bootstrap-select@1.13.9/dist/js/bootstrap-select.min.js',
        'https://cdn.jsdelivr.net/npm/select2@4.0.13/dist/js/select2.min.js',
        'https://unpkg.com/gijgo@1.9.13/js/gijgo.min.js',
    ]
]

default_logo = 'https://images.unsplash.com/photo-1534531173927-aeb928d54385?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80'
default_avatar = 'https://images.unsplash.com/photo-1494253109108-2e30c049369b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80'
default_cover = 'https://images.unsplash.com/photo-1494253109108-2e30c049369b?ixlib=rb-1.2.1&ixid=eyJhcHBfaWQiOjEyMDd9&auto=format&fit=crop&w=1350&q=80'


def upload(uploaded_file):
    """Process the uploaded file and upload it to Google Cloud Storage."""

    if not uploaded_file:
        return None

    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(app.config['CLOUD_STORAGE_BUCKET'])

    # Create a new blob and upload the file's content.
    blob = bucket.blob(uploaded_file.filename)

    blob.upload_from_string(
        uploaded_file.read(),
        content_type=uploaded_file.content_type
    )
    blob.make_public()

    # The public URL can be used to directly access the uploaded file via HTTP.
    return blob.public_url


def get_autopilot_schedule():
    # Create a Cloud Storage client.
    gcs = storage.Client()

    # Get the bucket that the file will be uploaded to.
    bucket = gcs.get_bucket(app.config['CLOUD_STORAGE_BUCKET_PRIVATE'])
    schedule = bucket.get_blob('schedule.xml')
    print(schedule)

    # The public URL can be used to directly access the uploaded file via HTTP.
    return schedule


class TagListField(Field):
    widget = widgets.TextInput()
    choices = []

    def process_formdata(self, valuelist):
        self.data = valuelist if valuelist else []

    def _value(self):
        print("_VALUE")
        return self.data if self.data is not None else []

    def __call__(self, **kwargs):
        options = []
        self.process_formdata(self.data)
        for choice in self.choices:
            if choice in self.data:
                options.append('<option selected="selected">{}</option>'.format(choice))
            else:
                options.append('<option>{}</option>'.format(choice))
        options = ''.join(options)
        field = '<select class="form-control js-example-tags" multiple="multiple" id="{}" name="{}">{}</select>'.format(
            self.name,
            self.name, options)

        return HTMLString(field)

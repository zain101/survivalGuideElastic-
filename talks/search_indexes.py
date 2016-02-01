import datetime
from haystack import indexes
from .models import Note


class NoteIndex(indexes.SearchIndex, indexes.Indexable):
    text = indexes.CharField(document=True, use_template=True)
    author = indexes.CharField(model_attr='user', faceted=True)
    pub_date = indexes.DateTimeField(model_attr='pub_date')
    # We add this for autocomplete.
    content_auto = indexes.EdgeNgramField(model_attr='body')
    suggestions = indexes.FacetCharField()

    def prepare(self, obj):
        prepared_data = super(NoteIndex, self).prepare(obj)
        prepared_data['suggestions'] = prepared_data['text']
        print "prepared_data: ", prepared_data
        return prepared_data

    def get_model(self):
        return Note

    def index_queryset(self, using=None):
        """Used when the entire index for model is updated."""
        return Note.objects.filter(pub_date__lte=datetime.datetime.now())

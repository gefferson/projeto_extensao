import os
import unicodedata

def get_upload_path(instance, filename):
    file = unicodedata.normalize('NFKD', filename).encode('ascii', 'ignore')
    filename = str(instance.pk)+'_%s' % file
    return os.path.join("pdf/%s" % (filename))
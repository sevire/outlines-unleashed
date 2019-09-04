import os

test_data_head = (
    ('version', '2.0'),
    ('title', 'Untitled 2'),
    ('dateCreated', None),
    ('dateModified', None),
    ('ownerName', None),
    ('ownerEmail', None),
    ('ownerId', None),
    ('docs', None),
    ('expansionState', ['16', '17', '31']),
    ('verticalScrollState', None),
    ('windowTop', 192),
    ('windowLeft', 0),
    ('windowBottom', 872),
    ('windowRight', 711)
)

test_resources_root = '../../resources'

test_data_version_filename = (
        (os.path.join(test_resources_root, 'opml-test-invalid-01.opml'), 'exception'),
        (os.path.join(test_resources_root, 'opml-test-invalid-02.opml'), 'exception'),
        (os.path.join(test_resources_root, 'opml-test-invalid-03.opml'), 'exception')
)

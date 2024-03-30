class Block:
    def __init__(self):
        self._block_type = None
        self._column_index = None
        self._column_span = None
        self._confidence = None
        self._entity_types = []
        self._geometry = None
        self._id = None
        self._page = None
        self._query = None
        self._relationships = []
        self._row_index = None
        self._row_span = None
        self._selection_status = None
        self._text = None
        self._text_type = None

    @property
    def block_type(self):
        return self._block_type

    @block_type.setter
    def block_type(self, value):
        self._block_type = value

    @property
    def column_index(self):
        return self._column_index

    @column_index.setter
    def column_index(self, value):
        self._column_index = value

    @property
    def column_span(self):
        return self._column_span

    @column_span.setter
    def column_span(self, value):
        self._column_span = value

    @property
    def confidence(self):
        return self._confidence

    @confidence.setter
    def confidence(self, value):
        self._confidence = value

    @property
    def entity_types(self):
        return self._entity_types

    @entity_types.setter
    def entity_types(self, value):
        self._entity_types = value

    @property
    def geometry(self):
        return self._geometry

    @geometry.setter
    def geometry(self, value):
        self._geometry = value

    @property
    def id(self):
        return self._id

    @id.setter
    def id(self, value):
        self._id = value

    @property
    def page(self):
        return self._page

    @page.setter
    def page(self, value):
        self._page = value

    @property
    def query(self):
        return self._query

    @query.setter
    def query(self, value):
        self._query = value

    @property
    def relationships(self):
        return self._relationships

    @relationships.setter
    def relationships(self, value):
        self._relationships = value

    @property
    def row_index(self):
        return self._row_index

    @row_index.setter
    def row_index(self, value):
        self._row_index = value

    @property
    def row_span(self):
        return self._row_span

    @row_span.setter
    def row_span(self, value):
        self._row_span = value

    @property
    def selection_status(self):
        return self._selection_status

    @selection_status.setter
    def selection_status(self, value):
        self._selection_status = value

    @property
    def text(self):
        return self._text

    @text.setter
    def text(self, value):
        self._text = value

    @property
    def text_type(self):
        return self._text_type

    @text_type.setter
    def text_type(self, value):
        self._text_type = value

    def is_set_block_type(self):
        return self._block_type is not None

    def is_set_column_index(self):
        return self._column_index is not None

    def is_set_column_span(self):
        return self._column_span is not None

    def is_set_confidence(self):
        return self._confidence is not None

    def is_set_entity_types(self):
        return bool(self._entity_types)

    def is_set_geometry(self):
        return self._geometry is not None

    def is_set_id(self):
        return self._id is not None

    def is_set_page(self):
        return self._page is not None

    def is_set_query(self):
        return self._query is not None

    def is_set_relationships(self):
        return bool(self._relationships)

    def is_set_row_index(self):
        return self._row_index is not None

    def is_set_row_span(self):
        return self._row_span is not None

    def is_set_selection_status(self):
        return self._selection_status is not None

    def is_set_text(self):
        return self._text is not None

    def is_set_text_type(self):
        return self._text_type is not None


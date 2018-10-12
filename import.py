from elasticsearch import Elasticsearch

es = Elasticsearch([{'host': 'localhost', 'port': 9200}])

def index(index, obj):
    es.index(index=index, doc_type='_doc', body=obj)

books = ['Matthew', 'Mark', 'Luke', 'John', 'Acts', 'Romans', '1 Corinthians', '2 Corinthians', 'Galatians', 'Ephesians', 'Philippians', 'Colossians', '1 Thessalonians', '2 Thessalonians', '1 Timothy', '2 Timothy', 'Titus', 'Philemon', 'Hebrews', 'James', '1 Peter', '2 Peter', '1 John', '2 John', '3 John', 'Jude', 'Revelation']
def verse_code_to_book(verse_code):
    return books[int(verse_code[0:2]) - 1]

def index_verse(verse_code, text, puncuationless_text, normalized_text, lexical_text, lexical_with_morph, morph_only):

    chapter = int(verse_code[2:4])
    verse = int(verse_code[4:6])

    index('morphgnt_verses', {
        'reference': verse_code_to_book(verse_code) + ' ' + str(chapter) + ':' + str(verse),
        'verse': verse_code,
        'book': verse_code_to_book(verse_code),
        'chapter': chapter,
        'verse': verse,
        'word_count': len(text.strip().split()),
        'text': text.strip(),
        'puncuationless_text': puncuationless_text.strip(),
        'normalized_text': normalized_text.strip(),
        'lexical_text': lexical_text.strip(),
        'morph_only': morph_only.strip(),
        'lexical_with_morph': lexical_with_morph.strip()
    })

def index_word(verse_code, pos, parsing, text, punctuationless, normalized, lexical):

    chapter = int(verse_code[2:4])
    verse = int(verse_code[4:6])

    index('morphgnt_words', {
        'reference': verse_code_to_book(verse_code) + ' ' + str(chapter) + ':' + str(verse),
        'pos': pos,
        'full_parsing': parsing,
        'person': parsing[0],
        'tense': parsing[1],
        'voice': parsing[2],
        'mood': parsing[3],
        'case': parsing[4],
        'number': parsing[5],
        'gender': parsing[6],
        'text': text,
        'punctuationless': punctuationless,
        'normalized': normalized,
        'lexical': lexical
    });

es.indices.delete(index='morphgnt_verses', ignore=[400, 404])
es.indices.delete(index='morphgnt_words', ignore=[400, 404])

files = ['81-1Pe-morphgnt', '82-2Pe-morphgnt', '83-1Jn-morphgnt', '86-Jud-morphgnt']
for filename in files:
    with open('./morphgnt/' + filename + '.txt') as f:
        content = f.readlines()
        content = [x.strip() for x in content]

        verse_code = ''
        text = ''
        puncuationless_text = ''
        normalized_text = ''
        lexical_text = ''
        morph_only = ''
        lexical_with_morph = ''

        for line in content:
            line_pieces = line.split()

            if verse_code == '':
                verse_code = line_pieces[0]
            elif verse_code != line_pieces[0]:
                index_verse(verse_code, text, puncuationless_text, normalized_text, lexical_text, lexical_with_morph, morph_only)
                verse_code = line_pieces[0]
                text = ''
                puncuationless_text = ''
                normalized_text = ''
                lexical_text = ''
                morph_only = ''
                lexical_with_morph = ''

            text = text + line_pieces[3] + ' '
            puncuationless_text = puncuationless_text + line_pieces[4] + ' '
            normalized_text = normalized_text + line_pieces[5] + ' '
            lexical_text = lexical_text + line_pieces[6] + ' '
            morph_only = morph_only + line_pieces[2] + ' '
            lexical_with_morph = lexical_with_morph + line_pieces[2] + '|' + line_pieces[6] + ' '

            index_word(line_pieces[0], line_pieces[1], line_pieces[2], line_pieces[3], line_pieces[4], line_pieces[5], line_pieces[6])

        index_verse(verse_code, text, puncuationless_text, normalized_text, lexical_text, lexical_with_morph, morph_only)

        #print(len(content))

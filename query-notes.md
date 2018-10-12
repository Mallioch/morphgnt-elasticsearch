
# Terminology

These are some things to refer back to re: querying. You don't have to understand all of this to start using Elasticsearch but as you try more queries, this will help you understand them better.

* `match` - by default, uses "or"
* `match_phrase` - in order, all must be matched
* `tokenization` -




# Sample Queries

## Basic Queries

### Find all occurrences of a word

* To match on the actual text, use the `text` field.
* To match on the actual text but without punctuation, use the `punctuationless_text` field.
* To match on a normalized inflected form, use the `normalized_text` field.
* To match on lexical forms, use the `lexical_text` field.

```
GET morphgnt_verses/_search
{
  "query": {
    "match": {
      "lexical_text": "ἔργον"
    }
  }
}
```

**Kibana Discover Tab**
* index: `morphgnt_verses`
* query: `lexical_text: "ἔργον"`

**Notes**

Query matches on a text field like above will search for that text *within* the field, not for records where the text exactly equals what is suppled. You can do that but we will get to that kind of query just below.

### Find all occurrences of either of two words

```
GET morphgnt_verses/_search
{
  "query": {
    "match": {
      "lexical_text": "ἔργον ἀλήθεια"
    }
  }
}
```

**Kibana Discover Tab**
* index: `morphgnt_verses`
* query: `lexical_text: (ἔργον || ἀλήθεια)`


### Find all occurrences two words anywhere in the same verse

```
GET morphgnt_verses/_search
{
  "query": {
    "match": {
      "lexical_text": {
        "query": "ἔργον ἀλήθεια",
        "operator": "and"
      }
    }
  }
}
```

**Kibana Discover Tab**
* index: `morphgnt_verses`
* query: `lexical_text: (ἔργον && ἀλήθεια)`

### Find all occurrences of a subset of a group of words

Let's say you want to query for three words but want to make sure at least two are present, but three is not necessary.

```
GET morphgnt_verses/_search
{
  "query": {
    "match": {
      "lexical_text": {
        "query": "θεός ἀγάπη εἰμί",
        "minimum_should_match": 2
      }
    }
  }
}
```

**Kibana Discover Tab**
Not sure if you can do this in the Kibana Discover tab.











### Get a verse

```
GET morphgnt_verses/_search
{
  "query": {
    "match": {
      "reference.keyword": "1 Peter 1:2"
    }
  }
}
```

**Kibana Discover Tab**
* index: `morphgnt_verses`
* query: `reference: "1 Peter 1:2"`

**Notes**

Note that the JSON query uses `reference.keyword` instead of just `reference`. If you remove that and run the search, you will find something interesting.

In Kibana, it does an exact search when the whole query is used. I am not sure why.

### Get a chapter of a book

```
GET morphgnt_verses/_search
{
  "query": {
    "bool": {
      "must": [
        { "match": {
            "book": "1 Peter"
          }
        },
        { "match": {
            "chapter": 2
          }
        }
      ]
    }
  }
}
```

**Kibana Discover Tab**
* index: `morphgnt_verses`
* query: `book: "1 Peter" && chapter: 2`

### Word with particular inflection - Way #1

Actually using the inflected form is probably an easier way to search for one that I will show you below (look for "Word with particular inflection - Way #2").

```
GET morphgnt_verses/_search
{
  "query": {
    "match": {
      "normalized_text": "ἀληθείᾳ"
    }
  }
}
```

**Kibana Discover Tab**
* index: `morphgnt_verses`
* query: `normalized_text: "ἀληθείᾳ"`

## Match Phrase


### Word with particular inflection - Way #2

If you want to search for the inflected form of a word using the lexical for and parsing values, you can use `match_phrase`. This will give you all verses that include "DSF|ἀλήθεια" and in that order.

```
GET morphgnt_verses/_search
{
  "query": {
    "match_phrase": {
      "lexical_with_morph": "DSF|ἀλήθεια"
    }
  }
}
```

The following query, which uses `match`, returns all results that have *either* "DSF" or "ἀλήθεια". This is because `match` will match on any available token, not all tokens. See the discussion of `match` `tokenization` above.

```
GET morphgnt_verses/_search
{
  "query": {
    "match": {
      "lexical_with_morph": "DSF|ἀλήθεια"
    }
  }
}
```

**Kibana Discover Tab**
* index: `morphgnt_verses`
* query: `lexical_with_morph: "DSF-|ἀλήθεια"`




## Aggregations


### Average words per verse

```
GET morphgnt_verses/_search
{
  "size": 0,
  "aggs": {
    "words_per_verse": {
      "avg": {
        "field": "word_count"
      }
    }
  }
}
```






### How often a word occurs by case

```
GET morphgnt_words/_search
{
  "size": 0,
  "query": {
    "match": {
      "lexical": "ὁ"
    }
  },
  "aggs": {
    "by_case": {
      "terms": {
        "field": "case.keyword"
      }
    }
  }
}
```


### Combine fields for aggregations if necessary

```
GET morphgnt_words/_search
{
  "size": 0,
  "query": {
    "match": {
      "lexical": "ὁ"
    }
  },
  "aggs": {
    "by_case": {
      "terms": {
        "script": {
        "source": "doc['case.keyword'].value + doc['number.keyword'].value"
        }
      }
    }
  }
}
```

# Wish List

* Combine words index into verses to...
  * agg on particular morphological characteristic



# Some Limitations

* Elasticsearch obviously can't break this text into clauses, so if you want clause-level searches, you'll need to create a separate index with data arranged that way.

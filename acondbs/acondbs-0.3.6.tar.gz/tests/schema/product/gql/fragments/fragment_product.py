FRAGMENT_PRODUCT = """
fragment fragmentProduct on Product {
  productId
  typeId
  type_ {
    typeId
    name
  }
  attributesUnicodeText {
    edges {
      node {
        name
        field {
          name
          type_
        }
        value
      }
    }
  }
  attributesBoolean {
    edges {
      node {
        name
        field {
          name
          type_
        }
        value
      }
    }
  }
  attributesInteger {
    edges {
      node {
        name
        field {
          name
          type_
        }
        value
      }
    }
  }
  attributesFloat {
    edges {
      node {
        name
        field {
          name
          type_
        }
        value
      }
    }
  }
  attributesDate {
    edges {
      node {
        name
        field {
          name
          type_
        }
        value
      }
    }
  }
  attributesDateTime {
    edges {
      node {
        name
        field {
          name
          type_
        }
        value
      }
    }
  }
  attributesTime {
    edges {
      node {
        name
        field {
          name
          type_
        }
        value
      }
    }
  }
  name
  contact
  dateProduced
  producedBy
  timePosted
  postedBy
  postingGitHubUser {
    login
  }
  timeUpdated
  updatedBy
  updatingGitHubUser {
    login
  }
  paths {
    edges {
      node {
        pathId
        path
        note
      }
    }
  }
  relations {
    edges {
      node {
        relationId
        typeId
        type_ {
          typeId
          name
        }
        otherProductId
        other {
          productId
          typeId
          type_ {
            typeId
            name
          }
          name
        }
        reverseRelationId
        reverse {
          relationId
          typeId
          type_ {
            typeId
            name
          }
        }
      }
    }
  }
  note
}
"""

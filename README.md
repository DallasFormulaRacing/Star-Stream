# Metrics Processor

Serverless Function to consume metrics from a Kafka topic and store them in Loki and MongoDB Time-Series.

### Loki Format
```json
{
  "streams": [
    {
      "stream": {
        "labelKey": "labelValue" # can be used for filtering
      },
      "values": [
        [
          "timestamp",
          "value"
          {"optional": "labels"}
        ]
      ]
    }
  ]
}
```

MongoDB Time-Series Format
```js
{
  "timestamp": "timestamp",
  "metadata": {
    "labelKey": "labelValue"
  }

  ...keyvalues
}
```

### Weird Hacks

- MongoDB is incredibly buggy so we are using certifi for SSL resolution.
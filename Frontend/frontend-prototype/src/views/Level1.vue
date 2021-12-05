<script>

const axios = require("axios");

export default {
  data() {
    return {
      info: 'Text',
    };
  },
  mounted() {
    const reqBody = {
      filter: [
        {
          attribute: "balance",
          lower_bound: 0,
          upper_bound: 0,
        },
        {
          attribute: "balance",
          values: ["string"],
        },
      ],
      attributes: ["amount", "duration", "balance", "age", "employment"],
      sort_by: "id",
      limit: 20,
      offset: 0,
    };

    axios.post("http://127.0.0.1:8000/table", reqBody).then((response) => (this.info = response)).catch(error => console.log(error));
  },
};
</script>

<template>
  <div>
    {{info}}
  </div>
</template>

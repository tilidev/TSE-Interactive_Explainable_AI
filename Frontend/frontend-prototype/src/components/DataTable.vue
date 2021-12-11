<template>
  <div class="q-pa-md">
    <q-table title="Data Table" :rows="rows" :columns="columns" row-key="id" />
  </div>
</template>

<script>
const axios = require("axios");

export default {
  data() {
    return {
      columns: [],
      rows: [],

      apiResponse: null,
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

    axios
      .post("http://localhost:8000" + "/table", reqBody)
      .then((response) => (this.apiResponse = response.data))
      .then(this.createColumnsAndRows)
      .catch((error) => console.log(error));
  },
  methods: {
    createColumnsAndRows() {
        for (const key of Object.keys(this.apiResponse[0])) {
            this.columns.push({
                name: key,
                label: key,
                field: key,
                sortable: true,
            }
            )
        }
        for (const row of this.apiResponse) {
            this.rows.push(row)
        }
    },
  },
};
</script>

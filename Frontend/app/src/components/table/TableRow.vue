<template>
  <tr><td v-for="value in rowData" :key="value">{{value}}</td></tr>
</template>

<script>
export default {
    props: {
        rowData: Object,
    }

}
</script>
<template>
  <div>
    <div id="treemap" />
  </div>
</template>

<script>
import * as d3 from "d3";
export default {
  components: {},
  name: "App4",
  data() {
    return {
      expType: "shap",
      result: {},
      detailView: true,
      simpleExpData: {
        positive: {
          name: "Attributes influencing towards approval",
          children: [],
        },
        negative: {
          name: "Attributes influencing towards rejection",
          children: [],
        },
      },
      detailExpData: {
        positive: {
          name: "Attributes influencing towards approval",
          children: [
            { name: "financial", children: [] },
            { name: "personal", children: [] },
            { name: "loan", children: [] },
          ],
        },
        negative: {
          name: "Attributes influencing towards rejection",
          children: [
            { name: "financial", children: [] },
            { name: "personal", children: [] },
            { name: "loan", children: [] },
          ],
        },
      },
      instance: {
        id: 0,
        balance: "no account",
        duration: 6,
        history: "paid back previous loans at this bank",
        purpose: "furniture",
        amount: 1169,
        savings: "above 1000 EUR",
        employment: "more than 7 years",
        available_income: "less than 20%",
        residence: "more than 7 years",
        assets: "real estate",
        age: 67,
        other_loans: "no additional loans",
        housing: "own",
        previous_loans: "2 or 3",
        job: "skilled",
        other_debtors: "none",
        people_liable: "0 to 2",
        telephone: "yes",
        NN_recommendation: "Approve",
        NN_confidence: 0.9382685422897339,
      },
    };
  },
  inject: ["attributeData", "apiUrl"],

  mounted() {
    this.sendExplanationRequest();
  },
  methods: {
    saveData(result) {
      for (let obj of result) {
        let childElement = {};
        childElement.name = this.attributeData.labels[obj.attribute];
        childElement.category = this.attributeData.categories[obj.attribute];
        childElement.value = Math.abs(obj.influence);
        let catObj;
        if (obj.influence < 0) {
          for (let category of this.detailExpData.negative.children) {
            if (
              category.name === this.attributeData.categories[obj.attribute]
            ) {
              catObj = category;
            }
          }
        } else {
          for (let category of this.detailExpData.positive.children) {
            if (
              category.name === this.attributeData.categories[obj.attribute]
            ) {
              catObj = category;
            }
          }
        }
        catObj.children.push(childElement);
      }
      for (let direction of ["negative", "positive"]) {
        console.log(this.detailExpData[direction].children);
        for (let category of this.detailExpData[direction].children) {
          let sum = 0;
          for (let attribute of category.children) {
            sum += attribute.value;
          }
          this.simpleExpData[direction].children.push({
            name: category.name,
            value: sum,
          });
        }
      }
      this.drawTreeMap();
    },
    getResult(href, result) {
      if (!result) {
        const axios = require("axios");
        axios
          .get(this.apiUrl + "explanations/" + this.expType + "?uid=" + href)
          .then((response) => {
            if (response.data.values) {
              result = response.data.values;
              this.saveData(result);
            }
          });
        setTimeout(() => this.getResult(href, result), 1000);
      }
      return result;
    },
    sendExplanationRequest() {
      const axios = require("axios");
      axios
        .post(this.apiUrl + "explanations/" + this.expType, {
          instance: this.instance,
        })
        .then((response) => {
          let href = response.data.href;
          this.getResult(href, null);
        });
    },
    drawTreeMap() {
      const w = 1000;
      const h = 900;
      let dataset = this.detailView
        ? this.detailExpData.positive
        : this.simpleExpData.positive;
      const hierarchy = d3
          .hierarchy(dataset)
          .sum((d) => d.value) //sums every child values
          .sort((a, b) => b.value - a.value), // and sort them in descending order
        treemap = d3.treemap().size([1000, 900]).padding(1),
        root = treemap(hierarchy);

      const categories = dataset.children.map((d) => d.name),
        colors = [
          "#1C1832",
          "#9E999D",
          "#F2259C",
          "#347EB4",
          "#08ACB6",
          "#91BB91",
          "#BCD32F",
          "#75EDB8",
          "#89EE4B",
          "#AD4FE8",
          "#D5AB61",
          "#BC3B3A",
          "#F6A1F9",
          "#87ABBB",
          "#412433",
          "#56B870",
          "#FDAB41",
          "#64624F",
        ],
        colorScale = d3
          .scaleOrdinal() // the scale function
          .domain(categories) // the data
          .range(colors); // the way the data should be shown

      const svg = d3
        .select("#treemap") //make sure there's a svg element in your html file
        .append("svg")
        .attr("width", w)
        .attr("height", h);

      svg
        .selectAll("rect")
        .data(root.leaves())
        .enter()
        .append("rect")
        .attr("x", (d) => d.x0)
        .attr("y", (d) => d.y0)
        .attr("width", (d) => d.x1 - d.x0)
        .attr("height", (d) => d.y1 - d.y0)
        .attr("fill", (d) => colorScale(d.data.category));
    },
  },
};
</script>
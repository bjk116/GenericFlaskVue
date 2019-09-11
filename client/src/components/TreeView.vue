<template>
  <div>
    <!--Search from scratch-->
    <!--     <b-row>
      <b-col>
        <b-alert
          :show="dismissCountDown === -1"
          variant="warning"
          dismissible
          fade
          @dismissed="dismissCountDown=0"
        >Please input a project number</b-alert>
        <b-alert
          :show="dismissCountDown"
          variant="info"
          fade
          @dismissed="dismissCountDown=0"
          @dismiss-count-down="countDownChanged"
        >
          <p>Searching...</p>
          <b-progress variant="warning" :max="dismissSecs" :value="dismissCountDown" height="4px"></b-progress>
        </b-alert>
      </b-col>
      <b-col>
        <b-form-input v-model="text" placeholder="Search a Project #"></b-form-input>
      </b-col>
    </b-row>-->
    <!--Tree  Structure From-->
    <b-row>
      <b-col class="treeRow">
        <Tree @updatedPath="handleSelection" @clearPath="clearPath" />
      </b-col>
    </b-row>
    <b-row>
      <b-col>
        <p v-show="showPath">
          <b>Path:</b>
          {{ currentPath }}
        </p>
      </b-col>
    </b-row>
  </div>
</template>

<script>
import Tree from "./Tree.vue";

export default {
  data() {
    return {
      currentPath: "",
      text: "",
      showPath: false,
      customerNumber: null,
    };
  },
  components: {
    Tree
  },
  methods: {
    handleSelection: function(payload) {
      console.log("HANDLING SELECTION IN TREE VIEW", payload);
      console.log(
        "typeof payload.value, about to set current path",
        typeof payload.value
      );
      console.log("payload value value", payload.value);
      this.currentPath = payload.value;
      console.log("just set current path", this.currentPath);
    },
    clearPath: function(node) {
      console.log("deslected Node", node);
      this.currentPath = "";
    }
  },
  watch: {
    currentPath: function() {
      console.log("PATH CHANGING");
      if (
        typeof this.currentPath == "undefined" ||
        this.currentPath.length == 0
      ) {
        console.log("hiding path");
        this.showPath = false;
      } else {
        console.log("showing path");
        this.showPath = true;
      }
    },
  },
};
</script>

<style>
.treeRow {
  margin-bottom: 200px;
}
</style>
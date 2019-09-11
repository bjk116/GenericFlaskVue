<template>
  <div id="tree">
    <treeselect
      v-model="value"
      :multiple="false"
      :options="options"
      :disableBranchNodes="false"
      :flatten-search-results="false"
      :alwaysOpen="true"
      :loading="true"
      :load-options="loadOptions"
      :maxHeight="200"
      @input="handleSelection"
    >
      <label
        slot="option-label"
        slot-scope="{ node, count, labelClassName, countClassName }"
        :class="labelClassName"
      ><b>{{ node.raw.otherProp }}:</b> {{ node.label }}</label>
    </treeselect>
  </div>
</template>

<script>
// import the component
import Treeselect from "@riophae/vue-treeselect";
// import the styles
import "@riophae/vue-treeselect/dist/vue-treeselect.css";
import axios from "axios";

export default {
  // register the component
  components: { Treeselect },
  data() {
    return {
      // define default value
      value: null,
      // define options
      options: null,
    };
  },
  methods: {
    loadOptions({ action, parentNode, callback }) {
      console.log("In loadoptions");
      console.log("action: ", action);
      if (action === "LOAD_ROOT_OPTIONS") {
        const path = "http://localhost:5000/customers/all";
        axios
          .get(path)
          .then(res => {
            this.options = res.data.customers;
            console.log("options");
            console.log(this.options);
            callback();
          })
          .catch(error => {
            // eslint-disable-next-line
            console.error(error);
          });
      }
      //if we are loading children locations
      else if (action === "LOAD_CHILDREN_OPTIONS") {
        console.log("attempting to load children for", parentNode);
        const parentTable =  parentNode.otherProp.toLowerCase();
        const idx = parentNode.dbId;
        const childrenPath = `http://localhost:5000/children/${parentTable}/${idx}`;
        console.log("Children path", childrenPath);
        axios
          .get(childrenPath)
          .then(res => {
            console.log("children payload: ", res.data.payload);
            parentNode.children = res.data.payload;
            callback();
          })
          .catch(error => {
            // eslint-disable-next-line
            console.error(error);
          });
      }
    },
    handleSelection(value, instanceId) {
      let payload = {'value':value, 'instId': instanceId};
      console.log("emitting from tree view payload", payload);
      this.$emit('updatedPath', payload);
    },
    clearSelection(node, instanceId) {
      this.$emit('clearPath', obj);
    }
  },
  watch: {
    value: function() {
      console.log("NEW VALUE", this.value);
    },
  }
  
};
</script>
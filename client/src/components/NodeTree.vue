<template>
  <li class="node-tree">
    <b-button v-b-toggle.collapse-1 variant="primary">+</b-button>
    <span class="label">{{ node.label }}</span>

    <ul v-if="node.children && node.children.length">
      <node v-for="child in node.children" :node="child"></node>
    </ul>
  </li>
</template>

<script>
export default {
  name: "node",
  props: {
    node: Object
  }
};
</script>
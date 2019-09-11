<template>
    <div>
		<b-row>
			<b-col>
				<TreeView />
			</b-col>
			<b-col>
				<Filters />
			</b-col>
		</b-row>
		<!--Table-->
		<b-row class="bumpDown">
			<b-col>
				<div class="tableHeight">
					<b-table :fields="fields" :items="items">
					</b-table>
				</div>
			</b-col>
		</b-row>
    </div>
</template>

<script>
import TreeView from '../TreeView.vue';
import Filters from '../Filters.vue';
import axios from "axios";

export default {
  components: {
	TreeView,
	Filters
  },
  data() {
	  return {
		  fields: ['Date', 'Entry Id', 'Project', 'Project #', 'Activity', 'Quantity', 'Sale Order', 'Invoice', 'Customer PO'],
		  items: [],
		  customerId: null,
	  }
  },
  methods:{
	getInitialRows() {
		console.log("getting inital rows");
		const path = "http://localhost:5000/timerecords/all";
        axios
          .get(path)
          .then(res => {
			console.log(res.data);
			this.items = res.data;
          })
          .catch(error => {
            // eslint-disable-next-line
            console.error(error);
          });
	},
  },
  created() {
	  this.getInitialRows();
  }
};
</script>

<style>
.tableHeight {
	height: 400px;
}
.bumpDown {
	margin-top: 2rem;
}
</style>
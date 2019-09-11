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
    </div>
</template>

<script>
import TreeView from '../TreeView.vue';
import Filters from '../Filters.vue';

export default {
  name: 'app',
  components: {
	TreeView,
	Filters
  },
};
</script>
<template>
  <div>
    <h5 class="text-center lead">Filters</h5>
    <h6>Edit Personal Filters</h6>
    <hr />
    <div v-if="['Home','TimeExpenseEntry'].indexOf($route.name) > -1">
      <b-form-row>
        <b-col>
          <p><b>Time Entry</b></p>
        </b-col>
        <b-col>
          <b-form-select :selected="selected" :options="EntryTypeOptions" class="xs-3"></b-form-select>
        </b-col>
        <b-col>
        </b-col>
        <b-col>
        </b-col>
      </b-form-row>
      
    </div>
    <div v-else-if="['Projects'].indexOf($route.name) > -1">
      <p> projectsfilters</p>
    </div>
    <div v-else-if="['CustomerMgmt'].indexOf($route.name) > -1">
      <p>Customer Management</p>
    </div>
    <div v-else-if="['VendorMgmt'].indexOf($route.name) > -1">
      <p>Vendor Management</p>
    </div>
    <div v-else-if="['Inventory'].indexOf($route.name) > -1">
      <p>Inventory</p>
    </div>
    <div v-else-if="['Quotes'].indexOf($route.name) > -1">
      <p>Quotes</p>
    </div>
  </div>
</template>

<script>
  export default {
    data() {
      return {
        selected: null,
        EntryTypeOptions: [
          { value: null, text: 'All'},
          { value: null, text: 'PSI Time Entry'},
          { value: null, text: 'PSI Expense Entry'}
        ]
      }
    },
    watch: {
      selected: function() {
        console.log("entry type selected:", this.selected);
      }
    }
  }
</script>
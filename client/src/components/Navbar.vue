<template>
  <div>
    <b-navbar toggleable="lg" type="dark" variant="primary">
      <b-navbar-brand :to="{name: 'Home'}">PSM4</b-navbar-brand>

      <b-navbar-toggle target="nav-collapse"></b-navbar-toggle>

      <b-collapse id="nav-collapse" is-nav>
        <b-navbar-nav>
          <b-nav-item :to="{ name: 'TimeSummary'}">Time Summary</router-link></b-nav-item>
          <b-nav-item :to="{ name: 'TimeExpenseEntry'}">Time/Expense Entry</b-nav-item>
          <b-nav-item :to="{ name: 'Projects'}">Projects</b-nav-item>
          <b-nav-item :to="{ name: 'CustomerMgmt'}">Customer Mgmt.</b-nav-item>
          <b-nav-item :to="{ name: 'VendorMgmt'}">Vendor Mgmt.</b-nav-item>
          <b-nav-item :to="{ name: 'Inventory'}">Inventory</b-nav-item>
          <b-nav-item :to="{ name: 'Quotes'}">Quotes</b-nav-item>
          <b-nav-item :to="{ name: 'Summary'}">Summary</b-nav-item>
          <b-nav-item :to="{ name: 'Settings'}">Global Settings</b-nav-item>
        </b-navbar-nav>

        <!-- Right aligned nav items -->
        <b-navbar-nav class="ml-auto">
            <b-navbar-nav>
                <b-nav-item :to="{ name: 'Login'}">Login</b-nav-item>
            </b-navbar-nav>
        </b-navbar-nav>
      </b-collapse>
    </b-navbar>
  </div>
</template>

<script>

</script>

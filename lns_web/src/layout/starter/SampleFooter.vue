<template>
  <footer class="footer">
    <div class="container-fluid">
      <div class="copyright">
        <a href="/terms-of-service.html">{{$t('site.terms_of_service')}}</a>
      </div>
    </div>
    <div class="container-fluid">
      <div class="copyright">
        <a href="/privacy-policy.html">{{$t('site.privacy_policy')}}</a>
      </div>
    </div>
    <div class="container-fluid">
      <div class="copyright">
        © {{year}} made with <i class="tim-icons icon-heart-2"></i> by
        <a href="https://www.iprogramstuff.com" target="_blank" rel="noopener">iProgramStuff</a>.
      </div>
    </div>
  </footer>
</template>
<script>
  export default {
    data() {
      return {
        year: new Date().getFullYear()
      }
    }
  };
</script>
<style>
</style>
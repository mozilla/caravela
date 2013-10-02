App.InsightController = Em.ObjectController.extend({
  needs: ["query"],
  /* needed so InsightController and PublicController can share the
  same template and view */
  chart: "insight.chart",
  describe: "insight.describe"
});

export const AxisBottom = (xScale, innerHeight, svgGroup) =>
  xScale.ticks().map((tickValue) => {
    const tickGroup = svgGroup
      .append("g")
      .attr("class", "tick")
      .attr("transform", `translate(${xScale(tickValue)},0)`);

    tickGroup.append("line").attr("y2", innerHeight);

    tickGroup
      .append("text")
      .attr("style", "text-anchor: middle")
      .attr("y", innerHeight + 3)
      .attr("dy", ".71em")
      .text(tickValue);
  });

export const AxisLeft = (yScale, svgGroup) => yScale.domain().map((tickValue) => {
    const tickGroup = svgGroup.append("g")
        .attr('class', 'tick');
    
    tickGroup.append('text')
        .attr('style', 'text-anchor: end')
        .attr('x', -3)
        .attr('y', yScale(tickValue) + yScale.bandwidth() / 2)
        .attr('dy', '.32em')
        .text(tickValue);
});
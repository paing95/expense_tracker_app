export const Marks = (data, svgGroup, xValue, xScale, yValue, yScale, xAxisTickFormat) => data.map((d) => {
    const rectangle = svgGroup.append("rect")
        .attr('class', 'mark')
        .attr('x', 0)
        .attr('y', yScale(yValue(d)))
        .attr('width', xScale(xValue(d)))
        .attr('height', yScale.bandwidth());
    
    rectangle.append('title')
        .text(xAxisTickFormat(xValue(d)));
});
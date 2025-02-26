export const Arcs = (data, arc, svgGroup, pie, color, radius) => {
    
    const arcs = svgGroup.selectAll("arc")
        .data(pie(Object.entries(data)))
        .enter()
        .append("g")
        .attr("class", "arc");
    
    arcs.append("path")
        .attr("fill", (d, i) => {
            return color(i)
        })
        .attr("d", arc);
    
    const label = d3.arc()
        .outerRadius(radius)
        .innerRadius(radius - 80);
    
    arcs.append('text')
        .attr("transform", function(d) { 
            const [x, y] = arc.centroid(d);
            const rotation = d.endAngle < Math.PI ? (d.startAngle / 2 + d.endAngle / 2) * 180 / Math.PI : (d.startAngle / 2 + d.endAngle / 2 + Math.PI) * 180 / Math.PI;
            return "translate(" + [x, y] + ") rotate(90) rotate(" + rotation + ")";
        })
        .text(d => d.data[1])
        .attr('fill', 'white');
}

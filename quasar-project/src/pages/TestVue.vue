<template>
  <q-page class="column">
    <div>
      <h4>{{ subhead }}</h4>
      <p>
        {{ msg }}
      </p>
      <div class="row q-pa-md">
        <div class="input-field">
          <q-input id="cities" v-model="nodes" />
          <label class="active" for="cities">Number of Nodes</label>
          <p>to be constructed : {{ nodes }}</p>
        </div>
        <q-btn class="waves-effect cyan darken-3" @click="constructGraph"
          >Construct</q-btn
        >
        <q-btn class="waves-effect grey darken-3 btn" @click="clearCanvas"
          >Clear</q-btn
        >
        <q-btn class="waves-effect red lighten-1 btn" @click="runGreedy"
          >Run</q-btn
        >
        <p>Optimal Solution : {{ greedySolution }}</p>
      </div>
      <div class="col s12 m10 l10" style="padding: 0px; height: 100%">
        <canvas ref="vCanvas" width="500" height="300" resize></canvas>
      </div>
    </div>
  </q-page>
</template>

<script>
import Paper from 'paper';
var canvas;
var listOfNodes = {};
var solutions = {};
var computedResult = [];
var adjacencyMatrix = {};
export default {
  name: 'greedyAl',
  data() {
    return {
      nodes: '',
      greedySolution: '',
      subhead: 'Greedy',
      msg: 'Greedy approach finds the solution by taking the least distance between cities',
    };
  },
  mounted: function () {
    canvas = this.$refs.vCanvas;
    canvas.style.backgroundColor = 'black';
    Paper.setup(canvas);
  },
  methods: {
    constructGraph: function () {
      var nodes = Number(this.nodes);
      if (nodes) {
        var canvasWidth = Paper.view.viewSize.width;
        var canvasHeight = Paper.view.viewSize.height;
        for (var j = 0; j < nodes; j++) {
          var randomX = getRandomInt(20, canvasWidth);
          var randomY = getRandomInt(20, canvasHeight);
          var nodeData = { x: randomX, y: randomY };
          listOfNodes[j] = nodeData;
          var point = new Paper.Point(randomX, randomY);
          var circle = new Paper.Path.Circle(point, 5);
          if (j === 0) {
            circle.fillColor = '#ff6c5d';
          } else {
            circle.fillColor = '#b2ebf2';
          }
          // console.log('Point ' + point + ' Nodes #' + j)
        }
        console.log(listOfNodes);
        for (var n = 0; n < nodes; n++) {
          var nodeA = new Paper.Point(listOfNodes[n].x, listOfNodes[n].y);
          var rowData = {};
          for (var k = 0; k < nodes; k++) {
            var nodeB = new Paper.Point(listOfNodes[k].x, listOfNodes[k].y);
            var distance = Math.round(nodeA.getDistance(nodeB));
            rowData[k] = distance;
          }
          adjacencyMatrix[n] = rowData;
        }
        console.log(adjacencyMatrix);
        Paper.view.draw();
      } else {
        alert('Nodes cannot be null');
      }
    },
    clearCanvas: function () {
      Paper.project.activeLayer.removeChildren();
    },
    runGreedy: function () {
      // Run Algorithm & Animations
      console.log('runGreedy function run');
      var i = 1;
      var m = 0;
      var tourCompleted = true;
      var solutionsCompleted = false;
      var solutionsComputationCompleted = false;
      var firstTour = true;
      var nodeCount = Object.keys(listOfNodes).length;
      var start;
      var end;
      var vect;
      var path = new Paper.Path();
      path.strokeColor = '#b2ebf2';
      Paper.view.onFrame = function (event) {
        if (!solutionsCompleted) {
          // Do algorithm & animations
          if (!tourCompleted) {
            // draw
            if (firstTour) {
              console.log('FirstTour');
              var firstNode = solutions[m][0];
              var secondNode = solutions[m][1];
              start = new Paper.Point(
                listOfNodes[firstNode].x,
                listOfNodes[firstNode].y
              );
              end = new Paper.Point(
                listOfNodes[secondNode].x,
                listOfNodes[secondNode].y
              );
              vect = end.subtract(start);
              vect = vect.normalize().multiply(7);
              firstTour = false;
            }
            if (start.isClose(end, 10)) {
              i++;
              if (i <= nodeCount) {
                // console.log('m , i : ' + m + ', ' + i)
                var nextNode = solutions[m][i];
                console.log('nextnode : ' + nextNode);
                end = new Paper.Point(
                  listOfNodes[nextNode].x,
                  listOfNodes[nextNode].y
                );
                vect = end.subtract(start);
                vect = vect.normalize().multiply(7);
              } else {
                i = 1;
                firstTour = true;
                tourCompleted = true;
                m++;
                path.remove();
                path = new Paper.Path();
                path.strokeColor = '#b2ebf2';
              }
            } else {
              path.add(start);
              start = start.add(vect);
            }
          } else {
            // compute next solution
            if (m < nodeCount) {
              var visited = [m];
              var cost = 0;
              for (var n = 0; n < nodeCount - 1; n++) {
                var result = checkNearestNode(
                  adjacencyMatrix,
                  visited[n],
                  nodeCount,
                  visited
                );
                cost += result[1];
                visited.push(result[0]);
              }
              visited.push(visited[0]);
              visited.push(cost);
              console.log('node : ' + visited);
              solutions[m] = visited;
              tourCompleted = false;
            } else {
              m = 0;
              solutionsCompleted = true;
            }
          }
        } else if (!solutionsComputationCompleted) {
          // draw final final result
          var solutionsLength = Object.keys(solutions).length;
          var leastTravelCost;
          var index;
          for (var k = 0; k < solutionsLength; k++) {
            var pathCost = solutions[k][nodeCount + 1];
            if (k === 0) {
              leastTravelCost = pathCost;
              index = k;
            } else if (leastTravelCost > pathCost) {
              leastTravelCost = pathCost;
              index = k;
            }
          }
          var finalPath = new Paper.Path();
          finalPath.strokeColor = '#49f24f';
          for (var j = 0; j < nodeCount; j++) {
            var currentNode = solutions[index][j];
            finalPath.add(
              new Paper.Point(
                listOfNodes[currentNode].x,
                listOfNodes[currentNode].y
              )
            );
          }
          finalPath.closed = true;
          computedResult.push(solutions[index]);
          computedResult[0].pop();
          this.greedySolution = computedResult.toString();
          alert(
            'Solution Path : \n ' +
              this.greedySolution +
              '\n Time Elapsed in s :\n' +
              event.time +
              ' s'
          );
          solutionsComputationCompleted = true;
        }
      };
    },
  },
};
function getRandomInt(min, max) {
  min = Math.ceil(min);
  max = Math.floor(max);
  return Math.floor(Math.random() * (max - min) + min);
}
function checkNearestNode(matrix, currentNode, nodeCount, path) {
  var leastCost = 0;
  var node;
  var firstTime = true;
  for (var i = 0; i < nodeCount; i++) {
    if (matrix[currentNode][i] === 0) {
      continue;
    } else if (path.includes(i)) {
      continue;
    } else {
      if (firstTime) {
        leastCost = matrix[currentNode][i];
        node = i;
        firstTime = false;
      } else {
        if (leastCost > matrix[currentNode][i]) {
          leastCost = matrix[currentNode][i];
          node = i;
        }
      }
    }
  }
  var result = [node, leastCost];
  return result;
}
</script>

<style scoped>
.row {
  padding: 0px;
  height: 100%;
}
p,
h4 {
  color: #bdbdbd;
}
input {
  color: #bdbdbd;
}
canvas[resize] {
  width: 100%;
  height: 100%;
}
/* label underline focus color */
.input-field input[type='text']:focus {
  border-bottom: 1px solid #00bcd4;
  box-shadow: 0 1px 0 0 #00bcd4;
}
</style>

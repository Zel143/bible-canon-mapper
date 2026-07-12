const fs = require('fs');

function main() {
  const inputPath = process.argv[2];
  const outputPath = process.argv[3];
  if (!inputPath || !outputPath) {
    console.error('Usage: node ua-tour-analyze.js <input.json> <output.json>');
    process.exit(1);
  }
  const raw = fs.readFileSync(inputPath, 'utf8');
  const data = JSON.parse(raw);
  const nodes = data.nodes || [];
  const edges = data.edges || [];
  const layers = data.layers || [];

  const nodeById = new Map();
  for (const n of nodes) nodeById.set(n.id, n);

  // Fan-in / fan-out
  const fanIn = new Map();
  const fanOut = new Map();
  for (const n of nodes) { fanIn.set(n.id, 0); fanOut.set(n.id, 0); }
  const adjForward = new Map(); // for BFS, only imports/calls
  for (const n of nodes) adjForward.set(n.id, []);

  for (const e of edges) {
    if (fanOut.has(e.source)) fanOut.set(e.source, fanOut.get(e.source) + 1);
    if (fanIn.has(e.target)) fanIn.set(e.target, fanIn.get(e.target) + 1);
    if ((e.type === 'imports' || e.type === 'calls' || e.type === 'depends_on') && adjForward.has(e.source)) {
      adjForward.get(e.source).push(e.target);
    }
  }

  const fanInRanking = nodes.map(n => ({ id: n.id, fanIn: fanIn.get(n.id) || 0, name: n.name }))
    .sort((a, b) => b.fanIn - a.fanIn).slice(0, 20);
  const fanOutRanking = nodes.map(n => ({ id: n.id, fanOut: fanOut.get(n.id) || 0, name: n.name }))
    .sort((a, b) => b.fanOut - a.fanOut).slice(0, 20);

  // Entry point candidates
  const fanOutValues = nodes.map(n => fanOut.get(n.id) || 0).sort((a, b) => b - a);
  const fanInValues = nodes.map(n => fanIn.get(n.id) || 0).sort((a, b) => a - b);
  const top10Idx = Math.max(0, Math.floor(nodes.length * 0.1) - 1);
  const bottom25Idx = Math.max(0, Math.floor(nodes.length * 0.25) - 1);
  const fanOutTop10Threshold = fanOutValues[top10Idx] !== undefined ? fanOutValues[top10Idx] : 0;
  const fanInBottom25Threshold = fanInValues[bottom25Idx] !== undefined ? fanInValues[bottom25Idx] : 0;

  const entryFilenames = new Set(['index.ts','index.js','main.ts','main.js','app.ts','app.js','server.ts','server.js','mod.rs','main.go','main.py','main.rs','manage.py','app.py','wsgi.py','asgi.py','run.py','__main__.py','Application.java','Main.java','Program.cs','config.ru','index.php','App.swift','Application.kt','main.cpp','main.c']);

  const entryPointCandidates = [];
  for (const n of nodes) {
    let score = 0;
    const filePath = n.filePath || '';
    const depth = filePath.split('/').filter(Boolean).length - 1;
    if (n.type === 'document') {
      if (filePath === 'README.md') score += 5;
      else if (/\.md$/.test(filePath) && depth === 0) score += 2;
    } else {
      if (entryFilenames.has(n.name)) score += 3;
      if (depth <= 1) score += 1;
      if ((fanOut.get(n.id) || 0) >= fanOutTop10Threshold && fanOutTop10Threshold > 0) score += 1;
      if ((fanIn.get(n.id) || 0) <= fanInBottom25Threshold) score += 1;
    }
    if (score > 0) entryPointCandidates.push({ id: n.id, score, name: n.name, summary: n.summary });
  }
  entryPointCandidates.sort((a, b) => b.score - a.score);
  const topEntryPointCandidates = entryPointCandidates.slice(0, 5);

  // BFS from top code entry point (skip document nodes)
  const codeEntry = entryPointCandidates.find(c => {
    const n = nodeById.get(c.id);
    return n && n.type !== 'document';
  });

  let bfsTraversal = { startNode: null, order: [], depthMap: {}, byDepth: {} };
  if (codeEntry) {
    const start = codeEntry.id;
    const visited = new Set([start]);
    const order = [start];
    const depthMap = { [start]: 0 };
    const queue = [start];
    while (queue.length) {
      const cur = queue.shift();
      const neighbors = adjForward.get(cur) || [];
      for (const nb of neighbors) {
        if (!visited.has(nb)) {
          visited.add(nb);
          order.push(nb);
          depthMap[nb] = depthMap[cur] + 1;
          queue.push(nb);
        }
      }
    }
    const byDepth = {};
    for (const [id, d] of Object.entries(depthMap)) {
      byDepth[d] = byDepth[d] || [];
      byDepth[d].push(id);
    }
    bfsTraversal = { startNode: start, order, depthMap, byDepth };
  }

  // Non-code file inventory
  const nonCodeFiles = { documentation: [], infrastructure: [], data: [], config: [] };
  for (const n of nodes) {
    if (n.type === 'document') nonCodeFiles.documentation.push({ id: n.id, name: n.name, summary: n.summary });
    else if (['service', 'pipeline', 'resource'].includes(n.type)) nonCodeFiles.infrastructure.push({ id: n.id, name: n.name, summary: n.summary });
    else if (['table', 'schema', 'endpoint'].includes(n.type)) nonCodeFiles.data.push({ id: n.id, name: n.name, summary: n.summary });
    else if (n.type === 'config') nonCodeFiles.config.push({ id: n.id, name: n.name, summary: n.summary });
  }

  // Clusters: bidirectional relationships expanded
  const edgeSet = new Set(edges.map(e => `${e.source}|||${e.target}|||${e.type}`));
  function hasEdge(a, b, type) { return edgeSet.has(`${a}|||${b}|||${type}`); }

  const pairEdgeCount = new Map();
  for (const e of edges) {
    const key = [e.source, e.target].sort().join('|||');
    pairEdgeCount.set(key, (pairEdgeCount.get(key) || 0) + 1);
  }

  const bidirPairs = [];
  for (const e of edges) {
    if ((e.type === 'imports' || e.type === 'calls') && hasEdge(e.target, e.source, e.type)) {
      bidirPairs.push([e.source, e.target]);
    }
  }

  const clusterSets = [];
  const usedNodes = new Set();
  for (const [a, b] of bidirPairs) {
    let found = clusterSets.find(c => c.has(a) || c.has(b));
    if (!found) {
      found = new Set();
      clusterSets.push(found);
    }
    found.add(a); found.add(b);
    usedNodes.add(a); usedNodes.add(b);
  }
  // Expand: add nodes connecting to 2+ existing members
  for (const cluster of clusterSets) {
    let changed = true;
    while (changed && cluster.size < 5) {
      changed = false;
      const counts = new Map();
      for (const e of edges) {
        if (cluster.has(e.target) && !cluster.has(e.source)) counts.set(e.source, (counts.get(e.source) || 0) + 1);
        if (cluster.has(e.source) && !cluster.has(e.target)) counts.set(e.target, (counts.get(e.target) || 0) + 1);
      }
      for (const [node, cnt] of counts.entries()) {
        if (cnt >= 2 && cluster.size < 5) {
          cluster.add(node);
          changed = true;
        }
      }
    }
  }
  const clusters = clusterSets.map(set => {
    const nodeArr = Array.from(set);
    let edgeCount = 0;
    for (const e of edges) {
      if (set.has(e.source) && set.has(e.target)) edgeCount++;
    }
    return { nodes: nodeArr, edgeCount };
  }).sort((a, b) => b.edgeCount - a.edgeCount).slice(0, 10);

  // Layers
  const layersOut = { count: layers.length, list: layers.map(l => ({ id: l.id, name: l.name, description: l.description })) };

  // Node summary index
  const nodeSummaryIndex = {};
  for (const n of nodes) nodeSummaryIndex[n.id] = { name: n.name, type: n.type, summary: n.summary };

  const result = {
    scriptCompleted: true,
    entryPointCandidates: topEntryPointCandidates,
    fanInRanking,
    fanOutRanking,
    bfsTraversal,
    nonCodeFiles,
    clusters,
    layers: layersOut,
    nodeSummaryIndex,
    totalNodes: nodes.length,
    totalEdges: edges.length
  };

  fs.writeFileSync(outputPath, JSON.stringify(result, null, 2), 'utf8');
  process.exit(0);
}

try {
  main();
} catch (err) {
  console.error(err && err.stack ? err.stack : String(err));
  process.exit(1);
}

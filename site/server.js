import express from 'express';
import cors from 'cors';
import { exec } from 'child_process';
import { fileURLToPath } from 'url';
import { dirname } from 'path';

const __filename = fileURLToPath(import.meta.url);
const __dirname = dirname(__filename);
const app = express();
app.use(cors());

app.get('/api/benchmark', (req, res) => {
  console.log('Running benchmark...');
  // We run the benchmark command and parse its output.
  // The command sets PYTHONPATH to the parent directory where `w` is located.
  const command = 'PYTHONPATH=.. python3 ../bench-p04-pcam/self_check.py --adapter w.adapters.myteam:Engine --quick';

  exec(command, { cwd: __dirname }, (error, stdout, stderr) => {
    if (error) {
      console.error(`exec error: ${error}`);
      return res.status(500).json({ error: error.message, stderr });
    }
    
    // Parse the stdout to extract the metrics
    try {
      const data = {
        totalWallTime: stdout.match(/total wall time\s+([\d.]+)\s+ms/)?.[1] || 'N/A',
        seeds: stdout.match(/seeds\s+(\d+)/)?.[1] || 'N/A',
        patterns: stdout.match(/stored patterns \(K\)\s+(\d+)/)?.[1] || 'N/A',
        stateDim: stdout.match(/state dim \(N\)\s+(\d+)/)?.[1] || 'N/A',
        noiseLevels: stdout.match(/noise levels\s+\[(.*?)\]/)?.[1] || 'N/A',
        meanDeltaAccuracy: stdout.match(/mean Δ accuracy \(over seeds\)\s+([+\-\d.]+)/)?.[1] || 'N/A',
        meanSpreadReduction: stdout.match(/mean spread reduction\s+([\d.]+)[x×]/)?.[1] || 'N/A',
        dynamicsPassRate: stdout.match(/dynamics-adds-value pass rate\s+([\d]+%)/)?.[1] || 'N/A',
        retrievalPts: stdout.match(/retrieval\s+\(max 70\)\s+([\d.]+)/)?.[1] || 'N/A',
        anisotropyPts: stdout.match(/anisotropy\s+\(max 20\)\s+([\d.]+)/)?.[1] || 'N/A',
        totalAutomated: stdout.match(/TOTAL AUTOMATED\s+([\d.]+)/)?.[1] || 'N/A',
        rawOutput: stdout
      };
      console.log('Benchmark finished!', data);
      res.json(data);
    } catch (e) {
      res.status(500).json({ error: 'Failed to parse output', details: e.message });
    }
  });
});

const PORT = 3001;
app.listen(PORT, () => {
  console.log(`Backend server running on http://localhost:${PORT}`);
});

import express, { Request, Response } from 'express';
import bodyParser from 'body-parser';
import multer from 'multer';
import { Canvas, Image, loadImage } from 'canvas';
import * as faceapi from '@vladmandic/face-api';

// Import your face.ts functions
import { loadModels, processImage } from './face';

// Extend Express Request to include multer file
interface MulterRequest extends Request {
  file?: Express.Multer.File;
}

const app = express();
const upload = multer();
const PORT = process.env.PORT || 8080;

// Middleware
app.use(bodyParser.json());

// Health check
app.get('/healthz', (_, res) => res.send('OK'));

// Endpoint: detect face in uploaded image
app.post('/detect_face', upload.single('image'), async (req: MulterRequest, res: Response) => {
  try {
    if (!req.file) return res.status(400).json({ error: 'No image uploaded' });

    // Convert buffer → Image
    const img = await loadImage(req.file.buffer);

    // Wrap as HTMLImageElement replacement
    const fakeElement: any = img; // face-api expects HTMLImageElement, node-canvas works as stub

    // Call your processImage logic
    const result = await processImage(fakeElement);

    if (!result) return res.json({ detections: [] });

    return res.json({
      box: result.detection.box,
      landmarks: result.landmarks,
      descriptor: Array.from(result.descriptor),
    });
  } catch (err) {
    console.error('Error in /detect_face:', err);
    return res.status(500).json({ error: 'Detection failed' });
  }
});

// Start server
app.listen(PORT, async () => {
  console.log(`Face recognition service running on port ${PORT}`);
  await loadModels();
});

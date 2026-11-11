import {Config} from '@remotion/cli/config';

// Saída padrão das redes (plano-mestre, seção 9.8): 1080×1920, 30 fps, H.264 + AAC.
Config.setVideoImageFormat('jpeg');
Config.setCodec('h264');
Config.setOverwriteOutput(true);

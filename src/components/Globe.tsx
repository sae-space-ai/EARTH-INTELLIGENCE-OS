import { useEffect, useRef, useState } from 'react';
import { Viewer } from 'resium';
import {
  Cartesian3,
  UrlTemplateImageryProvider,
  Ion
} from 'cesium';
import 'cesium/Build/Cesium/Widgets/widgets.css';

// Configure Cesium Ion (optional - works without token using keyless providers)
const cesiumToken = (window as any).__CESIUM_ION_TOKEN || '';
if (cesiumToken) {
  Ion.defaultAccessToken = cesiumToken;
}

interface GlobeProps {
  center?: { lon: number; lat: number; height?: number };
  trackedEntity?: string | null;
  visualStyle?: string;
  children?: React.ReactNode;
}

export function Globe({ center, trackedEntity, visualStyle = 'NORMAL', children }: GlobeProps) {
  const viewerRef = useRef<any>(null);
  const [viewerReady, setViewerReady] = useState(false);

  useEffect(() => {
    if (viewerRef.current && center) {
      const viewer = viewerRef.current.cesiumElement;
      if (viewer) {
        viewer.camera.flyTo({
          destination: Cartesian3.fromDegrees(center.lon, center.lat, center.height || 10000000),
          duration: 2,
        });
      }
    }
  }, [center]);

  return (
    <div className="relative w-full h-full">
      <Viewer
        ref={viewerRef}
        full
        //@ts-ignore - resium types are incomplete
        timeline={false}
        //@ts-ignore
        animation={false}
        //@ts-ignore
        baseLayerPicker={false}
        //@ts-ignore
        geocoder={false}
        //@ts-ignore
        homeButton={false}
        //@ts-ignore
        sceneModePicker={false}
        //@ts-ignore
        navigationHelpButton={false}
        //@ts-ignore
        fullscreenButton={false}
        //@ts-ignore
        infoBox={false}
        //@ts-ignore
        selectionIndicator={false}
        //@ts-ignore
        shadows={false}
        //@ts-ignore
        onReady={(viewer: any) => {
          viewerRef.current = { cesiumElement: viewer };
          setViewerReady(true);

          // Configure scene
          viewer.scene.globe.enableLighting = false;
          viewer.scene.skyAtmosphere.show = true;
          viewer.scene.fog.enabled = true;

          // Add Esri World Imagery (keyless)
          const esriProvider = new UrlTemplateImageryProvider({
            url: 'https://server.arcgisonline.com/ArcGIS/rest/services/World_Imagery/MapServer/tile/{z}/{y}/{x}',
            credit: 'Powered by Esri — Source: Esri, Maxar, Earthstar Geographics',
          });
          viewer.imageryLayers.addImageryProvider(esriProvider);
        }}
      >
        {children}
      </Viewer>

      {/* Visual style overlay */}
      {visualStyle !== 'NORMAL' && (
        <div
          className="absolute inset-0 pointer-events-none mix-blend-multiply"
          style={{
            background: visualStyle === 'NVG'
              ? 'radial-gradient(ellipse at center, rgba(0,255,0,0.1) 0%, rgba(0,50,0,0.3) 100%)'
              : visualStyle === 'FLIR'
              ? 'radial-gradient(ellipse at center, rgba(255,100,0,0.1) 0%, rgba(50,0,50,0.3) 100%)'
              : visualStyle === 'CRT'
              ? 'repeating-linear-gradient(0deg, rgba(0,0,0,0.1) 0px, rgba(0,0,0,0.1) 1px, transparent 1px, transparent 2px)'
              : 'none',
          }}
        />
      )}
    </div>
  );
}

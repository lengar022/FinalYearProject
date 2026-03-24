<script lang="ts">
	import 'leaflet/dist/leaflet.css';
	import { onMount } from 'svelte';
	import type { Map as LeafletMap, TileLayer, LayerGroup, Marker } from 'leaflet';

	let { height, id, latitude, longitude, zoom, name, path } = $props();

	let map: LeafletMap;
	let marker: Marker;
    let pathLayer: LayerGroup;
	let baseLayer: TileLayer;
	let L: any;

    function isValid(coord) {
		return typeof coord === 'number' && !isNaN(coord);
	}

	onMount(async () => {
		const leaflet = await import('leaflet');
		L = leaflet.default;

        if (!isValid(latitude) || !isValid(longitude)) return;

		baseLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			maxZoom: 19,
			attribution: '&copy; OpenStreetMap contributors'
		});

		map = L.map(id, {
			center: [latitude, longitude],
			zoom: zoom || 15,
			layers: [baseLayer]
		});

        pathLayer = L.layerGroup().addTo(map);
        marker = L.circleMarker([latitude, longitude], {
			radius: 8,
			color: 'white',
			fillColor: 'blue',
			fillOpacity: 1
		}).addTo(map);
		marker.bindPopup(name);
	});

	$effect(() => {
	    console.log('map props changed', latitude, longitude);
		if (map && marker) {
            if (!isValid(latitude) || !isValid(longitude)) return;

            pathLayer.clearLayers();

            if (path.length > 1) {
                for (let i = 0; i < path.length - 1; i++) {
                    const point = path[i];

                    if (isValid(point.lat) && isValid(point.lon)) {
                        L.circleMarker([point.lat, point.lon], {
                            radius: 4,
                            color: 'red',
                            fillColor: 'red',
                            fillOpacity: 0.8,
                            weight: 1
                        }).addTo(pathLayer);
                    }
                }
            }

            marker.setLatLng([latitude, longitude]);
	        map.setView([latitude, longitude], map.getZoom());
        }
    });
</script>

<div id={id} class="box" style={`height: ${height};`}></div>

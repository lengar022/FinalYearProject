<script lang="ts">
	import 'leaflet/dist/leaflet.css';
	import { onMount } from 'svelte';
	import type { Map as LeafletMap, TileLayer, Marker } from 'leaflet';

	let {
		height = '500px',
		id = 'telemetry-map',
		latitude = 52.245,
		longitude = -7.139,
		zoom = 13,
		name = 'Car Location'
	} = $props();

	let map: LeafletMap;
	let marker: Marker;
	let baseLayer: TileLayer;
	let L: any;

	onMount(async () => {
		const leaflet = await import('leaflet');
		L = leaflet.default;

		baseLayer = L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
			maxZoom: 19,
			attribution: '&copy; OpenStreetMap contributors'
		});

		map = L.map(id, {
			center: [latitude, longitude],
			zoom,
			layers: [baseLayer]
		});

		marker = L.marker([latitude, longitude]).addTo(map);
		marker.bindPopup(name);
	});

	$effect(() => {
        if (map && marker) {
            map.setView([latitude, longitude], zoom);
            marker.setLatLng([latitude, longitude]);
        }
    });
</script>

<div {id} class="box" style={`height: ${height};`}></div>

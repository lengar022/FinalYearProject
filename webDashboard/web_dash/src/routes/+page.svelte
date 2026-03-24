<script>
	import LeafletMap from "$lib/ui/LeafletMap.svelte";
	import mqtt from 'mqtt';
		
	let telemetry = $state({
		engine: { water_temp: null },
		fuel: { percent: null },
		gps: { fix: false, lat: null, lon: null, speed_kph: null },
		tpms: {
			front_left: { psi: null, temp: null },
			front_right: { psi: null, temp: null },
			rear_left: { psi: null, temp: null },
			rear_right: { psi: null, temp: null }
		}
	});

	let gpsPath = $state([]);

	function display(value, suffix = '') {
		return value === null || value === undefined ? '--' : `${value}${suffix}`;
	}

	function isLowPressure(psi) {
		return psi !== null && psi !== undefined && psi < 20;
	}

	function isTempHigh(water_temp) {
		return water_temp !== null && water_temp !== undefined && water_temp > 90;
	}

	function isFuelLow(fuel_level) {
		return fuel_level !== null && fuel_level !== undefined && fuel_level < 20;
	}

	function samePoint(a, b) {
		return a && b && a.lat === b.lat && a.lon === b.lon;
	}

	const client = mqtt.connect('wss://5add9226d618439896fb79c33b12c919.s1.eu.hivemq.cloud:8884/mqtt', {
		username: 'lengar022',
		password: 'e75izM_fvYzt4WX',
		reconnectPeriod: 3000,
		connectTimeout: 10000
	});

	client.on('connect', () => {
		client.subscribe('car/telemetry/live', (err) => {
			if (err) {
				console.error('Subscribe error:', err);
			}
		});
	});

	client.on('message', (_topic, message) => {
		try {
			const data = JSON.parse(message.toString());

			telemetry = {
				engine: data.engine,
				fuel: data.fuel,
				tpms: data.tpms,
				gps: {
					fix: data.gps?.fix ?? false,
					lat: data.gps?.lat != null ? Number(data.gps.lat) : null,
					lon: data.gps?.lon != null ? Number(data.gps.lon) : null,
					speed_kph: data.gps?.speed_kph ?? null
				}
			};

			if (typeof telemetry.gps.lat === 'number' && typeof telemetry.gps.lon === 'number') {
				const latestPoint = {
					lat: telemetry.gps.lat,
					lon: telemetry.gps.lon
				};

				const lastPoint = gpsPath[gpsPath.length - 1];

				if (!samePoint(lastPoint, latestPoint)) {
					gpsPath = [...gpsPath, latestPoint];
				}
			}

		} catch (err) {
			console.error('Bad MQTT payload:', err);
		}
	});

</script>

<section class="section">
	<div class="container">
		<div class="box has-text-centered">
			<h1 class="title">Car Telemetry Dashboard</h1>
			<p class="subtitle">Dashboard layout with placeholder telemetry values</p>
		</div>

		<div class="columns is-multiline">
			<div class="column is-4">
				<div class="card">
					<header class="card-header">
						<p class="card-header-title is-size-4">Engine & Fuel</p>
					</header>

					<div class="card-content">
						<div class="columns">
							<div class="column">
								<div class="box has-text-centered {isTempHigh(telemetry.engine?.water_temp) ? 'flash-red' : ''}">
									<p class="heading">Water Temp</p>
									<p class="title is-4">{display(telemetry.engine?.water_temp, ' °C')}</p>
								</div>
							</div>

							<div class="column">
								<div class="box has-text-centered {isFuelLow(telemetry.fuel?.percent) ? 'flash-red' : ''}">
									<p class="heading">Fuel %</p>
									<p class="title is-4">{display(telemetry.fuel?.percent, ' %')}</p>
								</div>
							</div>
						</div>
					</div>
				</div>

				<div class="card">
					<header class="card-header">
						<p class="card-header-title is-size-4">TPMS</p>
					</header>

					<div class="card-content">
						<div class="columns is-multiline">
							<div class="column is-6">
								<div class="box has-text-centered {isLowPressure(telemetry.tpms?.front_left?.psi) ? 'flash-red' : ''}">
									<p class="heading">Front Left</p>
									<p class="title is-5">{display(telemetry.tpms?.front_left?.psi, ' PSI')}</p>
									<p class="subtitle is-6">{display(telemetry.tpms?.front_left?.temp, ' °C')}</p>
								</div>
							</div>

							<div class="column is-6">
								<div class="box has-text-centered {isLowPressure(telemetry.tpms?.front_right?.psi) ? 'flash-red' : ''}">
									<p class="heading">Front Right</p>
									<p class="title is-5">{display(telemetry.tpms?.front_right?.psi, ' PSI')}</p>
									<p class="subtitle is-6">{display(telemetry.tpms?.front_right?.temp, ' °C')}</p>
								</div>
							</div>

							<div class="column is-6">
								<div class="box has-text-centered {isLowPressure(telemetry.tpms?.rear_left?.psi) ? 'flash-red' : ''}">
									<p class="heading">Rear Left</p>
									<p class="title is-5">{display(telemetry.tpms?.rear_left?.psi, ' PSI')}</p>
									<p class="subtitle is-6">{display(telemetry.tpms?.rear_left?.temp, ' °C')}</p>
								</div>
							</div>

							<div class="column is-6">
								<div class="box has-text-centered {isLowPressure(telemetry.tpms?.rear_right?.psi) ? 'flash-red' : ''}">
									<p class="heading">Rear Right</p>
									<p class="title is-5">{display(telemetry.tpms?.rear_right?.psi, ' PSI')}</p>
									<p class="subtitle is-6">{display(telemetry.tpms?.rear_right?.temp, ' °C')}</p>
								</div>
							</div>
						</div>
					</div>
				</div>
			</div>

			<div class="column is-8">

				<div class="card">
					<header class="card-header">
						<p class="card-header-title is-size-4">GPS</p>
					</header>

					<div class="card-content">
						<div class="columns">
							<div class="column">
								<div class="box has-text-centered">
									<p class="heading">Latitude</p>
									<p class="title is-5">{display(telemetry.gps?.lat)}</p>
								</div>
							</div>

							<div class="column">
								<div class="box has-text-centered">
									<p class="heading">Longitude</p>
									<p class="title is-5">{display(telemetry.gps?.lon)}</p>
								</div>
							</div>

							<div class="column">
								<div class="box has-text-centered">
									<p class="heading">Speed</p>
									<p class="title is-5">{display(telemetry.gps?.speed_kph, ' km/h')}</p>
								</div>
							</div>

							<div class="column">
								<div class="box has-text-centered">
									<p class="heading">GPS Fix</p>
									<p class="title is-5">{telemetry.gps?.fix ? 'Yes' : 'No'}</p>
								</div>
							</div>
						</div>
					</div>
				</div>
				<div class="card">
					<header class="card-header">
						<p class="card-header-title is-size-4">Live Location</p>
					</header>
					<div class="card-content">
					{#if typeof telemetry.gps?.lat === 'number' && typeof telemetry.gps?.lon === 'number'}
						<LeafletMap
							height="500px"
							id="main-map"
							latitude={telemetry.gps.lat}
							longitude={telemetry.gps.lon}
							zoom={15}
							name="Rally Car"
							path={gpsPath}
						/>
					{:else}
						<div class="box has-text-centered">
							<p class="title is-5">No GPS fix yet</p>
						</div>
					{/if}
					</div>
				</div>
			</div>
		</div>
	</div>
</section>

<style>
	@keyframes flash-red {
		0% { background-color: #fff; }
		50% { background-color: #ffe5e5; }
		100% { background-color: #fff; }
	}

	.flash-red {
		animation: flash-red 1s infinite;
	}
</style>
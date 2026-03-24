<script>
	import LeafletMap from "$lib/ui/LeafletMap.svelte";
		
	let telemetry = {
		engine: { water_temp: 91 },
		fuel: { percent: 65 },
		gps: { fix: true, lat: 52.245, lon: -7.139, speed_kph: 74 },
		tpms: {
			front_left: { psi: 18.5, temp: 31 },
			front_right: { psi: 28.9, temp: 30 },
			rear_left: { psi: 27.8, temp: 29 },
			rear_right: { psi: 28.1, temp: 30 }
		}
	};

	function display(value, suffix = '') {
		return `${value}${suffix}`;
	}

	function isLowPressure(psi) {
		return psi !== null && psi < 20;
	}

	function isTempHigh(water_temp) {
		return water_temp !== null && water_temp > 90;
	}

	function isFuelLow(fuel_level) {
		return fuel_level !== null && fuel_level < 20;
	}

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

				<div class="card mb-5">
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
						<p class="card-header-title is-size-4">Live Location</p>
					</header>
					<div class="card-content">
						<LeafletMap
							height="437px"
							id="main-map"
							latitude={telemetry.gps.lat}
							longitude={telemetry.gps.lon}
							zoom={13}
							name="Rally Car"
						/>
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
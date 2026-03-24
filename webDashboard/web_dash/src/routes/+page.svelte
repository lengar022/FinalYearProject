<script>
	import LeafletMap from "$lib/ui/LeafletMap.svelte";
		
	let telemetry = {
		engine: { water_temp: 88 },
		fuel: { percent: 62 },
		gps: { fix: true, lat: 52.245, lon: -7.139, speed_kph: 74 },
		tpms: {
			front_left: { psi: 28.5, temp: 31 },
			front_right: { psi: 28.9, temp: 30 },
			rear_left: { psi: 27.8, temp: 29 },
			rear_right: { psi: 28.1, temp: 30 }
		}
	};

	function display(value, suffix = '') {
		return `${value}${suffix}`;
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
								<div class="box has-text-centered">
									<p class="heading">Water Temp</p>
									<p class="title is-4">{display(telemetry.engine?.water_temp, ' °C')}</p>
								</div>
							</div>

							<div class="column">
								<div class="box has-text-centered">
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
								<div class="box has-text-centered">
									<p class="heading">Front Left</p>
									<p class="title is-5">{display(telemetry.tpms?.front_left?.psi, ' PSI')}</p>
									<p class="subtitle is-6">{display(telemetry.tpms?.front_left?.temp, ' °C')}</p>
								</div>
							</div>

							<div class="column is-6">
								<div class="box has-text-centered">
									<p class="heading">Front Right</p>
									<p class="title is-5">{display(telemetry.tpms?.front_right?.psi, ' PSI')}</p>
									<p class="subtitle is-6">{display(telemetry.tpms?.front_right?.temp, ' °C')}</p>
								</div>
							</div>

							<div class="column is-6">
								<div class="box has-text-centered">
									<p class="heading">Rear Left</p>
									<p class="title is-5">{display(telemetry.tpms?.rear_left?.psi, ' PSI')}</p>
									<p class="subtitle is-6">{display(telemetry.tpms?.rear_left?.temp, ' °C')}</p>
								</div>
							</div>

							<div class="column is-6">
								<div class="box has-text-centered">
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
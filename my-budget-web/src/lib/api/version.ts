export async function fetchBuildInfo(apiUrl: string) {
	try {
		const response = await fetch(`${apiUrl}/version`);
		const buildInfo = await response.json();
		return buildInfo;
	} catch (error) {
		console.error('Error fetching Categories:', error);
		throw error; // Rethrow the error so the calling function can handle it
	}
}

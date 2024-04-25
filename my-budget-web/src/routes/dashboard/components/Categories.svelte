<script lang="ts">
	import { onMount } from 'svelte';
	import { toast } from 'svelte-french-toast';
	import {
		fetchCategories,
		createCategory,
		deleteCategory,
		updateCategory
	} from '$lib/api/categories';
	import type { Category, CategoryCreateRequest } from '../../../types/types';
	import { categoriesStore } from '$lib/store';
	import * as Table from '$lib/components/ui/table';
	import { Button } from '$lib/components/ui/button'; // Assume you have this component
	import * as Card from '$lib/components/ui/card'; // Assume you have this component
	import { Input } from '$lib/components/ui/input';
	import { Label } from '$lib/components/ui/label';
	import { writable } from 'svelte/store';

	let categories = $categoriesStore;
	let showModal = writable(false);
	let creatingCategory = writable(false);
	let newCategory: CategoryCreateRequest = {
		name: '',
		budgeted_amount: 0,
		budgeted_limit: 0,
		color_code: '',
		description: '',
		icon: ''
	};

	categoriesStore.subscribe((value) => {
		categories = value;
	});
	function getColorOrRandom(colorCode: string): string {
		if (
			!colorCode ||
			colorCode.toLowerCase() === '#ffffff' ||
			colorCode.toLowerCase() === 'white' ||
			colorCode.toLowerCase() === 'string'
		) {
			return `#${Math.floor(Math.random() * 16777215).toString(16)}`; // Generate a random hex color
		}
		return colorCode;
	}

	async function handleCreateCategory() {
		const token = localStorage.getItem('access_token');
		if (!token) {
			toast.error('You must be logged in to create categories.');
			return;
		}

		try {
			const createdCategory = await createCategory(
				import.meta.env.VITE_API_URL,
				token,
				newCategory
			);
			categories = [
				...categories,
				{ ...createdCategory, color_code: getColorOrRandom(createdCategory.color_code) }
			];
			categoriesStore.set(categories);
			toast.success('Category created successfully.');
			creatingCategory.set(false); // Hide the form after successful creation
		} catch (error) {
			console.error('Error creating category:', error);
			toast.error('Failed to create category.');
		}

		// clear the form after creating a category
		newCategory = {
			name: '',
			budgeted_amount: 0,
			budgeted_limit: 0,
			color_code: '',
			description: '',
			icon: ''
		};

		creatingCategory.set(false);
	}

	function handleCancel() {
		creatingCategory.set(false);
	}

	async function handleDeleteCategory(categoryId: number) {
		const token = localStorage.getItem('access_token');
		if (!token) {
			toast.error('You must be logged in to delete categories.');
			return;
		}

		try {
			await deleteCategory(import.meta.env.VITE_API_URL, token, categoryId);
			// Filter out the deleted category from the state and update
			categories = categories.filter((category) => category.id !== categoryId);
			categoriesStore.set(categories); // Update the store
			toast.success('Category deleted successfully.');
		} catch (error) {
			toast.error('Failed to delete category');
		}
	}

	// create edit modal to edit category
	let showEditModalState = false;
	let editingCategory: Category | null = null;

	function showEditModal(category: Category) {
		editingCategory = category;
		showEditModalState = true;
	}

	// Define the handleEditSubmit function to handle the edit form submission
	async function handleEditSubmit() {
		if (!editingCategory) return;

		const token = localStorage.getItem('access_token');
		if (!token) {
			toast.error('You must be logged in to edit categories.');
			return;
		}

		try {
			const updatedCategory = await updateCategory(
				import.meta.env.VITE_API_URL,
				token,
				editingCategory.id,
				{
					name: editingCategory.name,
					budgeted_amount: editingCategory.budgeted_amount,
					budgeted_limit: editingCategory.budgeted_limit,
					color_code: editingCategory.color_code,
					description: editingCategory.description,
					icon: editingCategory.icon
				}
			);
			// Update the categories array with the updated category
			categories = categories.map((category) =>
				category.id === updatedCategory.id ? updatedCategory : category
			);
			categoriesStore.set(categories); // Update the store
			toast.success('Category updated successfully.');
			showEditModalState = false; // Hide the modal after successful update
		} catch (error) {
			console.error('Error updating category:', error);
			toast.error('Failed to update category.');
		}
	}

	onMount(async () => {
		const token = localStorage.getItem('access_token');
		if (token) {
			try {
				let fetchedCategories = await fetchCategories(import.meta.env.VITE_API_URL, token);
				fetchedCategories = fetchedCategories.map((category: Category) => ({
					...category,
					color_code: getColorOrRandom(category.color_code)
				}));
				categoriesStore.set(fetchedCategories);
				categories = fetchedCategories;
			} catch (error) {
				console.error('Error fetching categories:', error);
				toast.error('Failed to fetch categories.');
			}
		} else {
			toast.error('You must be logged in to view categories.');
		}
	});
</script>

<div class="container mx-auto px-4 py-6">
	<div class="flex justify-between items-center mb-4">
		<h2 class="text-xl font-semibold">Budget Categories</h2>
		<Button on:click={() => creatingCategory.set(true)}>Add New Category</Button>
	</div>

	<Table.Root>
		<Table.Header>
			<Table.Row>
				<Table.Head>Category Name</Table.Head>
				<!-- <Table.Head>ID</Table.Head> -->
				<Table.Head>Budget Limit</Table.Head>
				<Table.Head>Budget Spent</Table.Head>
				<Table.Head>Budget Remaining</Table.Head>
				<!-- <Table.Head>Is Active</Table.Head> -->
				<Table.Head>Description</Table.Head>
			</Table.Row>
		</Table.Header>
		<Table.Body>
			{#each categories as category (category.id)}
				<Table.Row>
					<Table.Cell
						style="background-color: {category.color_code}; color: {category.color_code.toLowerCase() ===
						'#ffffff'
							? 'black'
							: 'white'};"
					>
						{category.name}
					</Table.Cell>
					<!-- <Table.Cell>{category.id}</Table.Cell> -->
					<Table.Cell>${category.budgeted_amount}</Table.Cell>
					<Table.Cell>${category.budgeted_limit}</Table.Cell>
					<Table.Cell>{category.is_active ? 'Yes' : 'No'}</Table.Cell>
					<Table.Cell>{category.description}</Table.Cell>
					<Table.Cell class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
						<Button variant="destructive" on:click={() => handleDeleteCategory(category.id)}
							>Delete</Button
						>
						<Button variant="outline" on:click={() => showEditModal(category)}>Edit</Button>
					</Table.Cell>
				</Table.Row>
			{/each}
		</Table.Body>
	</Table.Root>
</div>

{#if $creatingCategory}
	<!-- Overlay -->
	<div class="fixed inset-0 bg-gray-600 bg-opacity-50 z-40"></div>

	<!-- Modal -->
	<div class="fixed inset-0 z-50 overflow-y-auto flex justify-center items-center">
		<Card.Root
			class="w-full max-w-lg m-4  rounded-lg overflow-hidden shadow-2xl transform transition-all"
		>
			<Card.Header>
				<Card.Title>Add New Category</Card.Title>
			</Card.Header>
			<Card.Content>
				<form class="space-y-4">
					<div>
						<Label for="name">Category Name</Label>
						<Input id="name" placeholder="Enter category name" bind:value={newCategory.name} />
					</div>
					<div>
						<Label for="budgeted_amount">Budgeted Limit</Label>
						<Input
							id="budgeted_amount"
							type="number"
							placeholder="Enter budgeted amount"
							bind:value={newCategory.budgeted_amount}
						/>
					</div>
					<div>
						<Label for="color_code">Color Code</Label>
						<Input
							id="color_code"
							type="text"
							placeholder="Enter color code"
							bind:value={newCategory.color_code}
						/>
					</div>
					<div>
						<Label for="description">Description</Label>
						<Input
							id="description"
							type="text"
							placeholder="Enter description"
							bind:value={newCategory.description}
						/>
					</div>
				</form>
			</Card.Content>
			<Card.Footer class="flex justify-end space-x-2">
				<Button variant="outline" on:click={handleCancel}>Cancel</Button>
				<Button on:click={handleCreateCategory}>Create</Button>
			</Card.Footer>
		</Card.Root>
	</div>
{/if}
{#if showEditModalState && editingCategory}
	<!-- Overlay -->
	<div class="fixed inset-0 bg-gray-600 bg-opacity-50 z-40"></div>

	<!-- Modal -->
	<div class="fixed inset-0 z-50 overflow-y-auto flex justify-center items-center">
		<Card.Root
			class="w-full max-w-lg m-4  rounded-lg overflow-hidden shadow-2xl transform transition-all"
		>
			<Card.Header>
				<Card.Title>Edit Category</Card.Title>
			</Card.Header>
			<Card.Content>
				<form class="space-y-4">
					<div>
						<Label for="name">Category Name</Label>
						<Input id="name" placeholder="Enter category name" bind:value={editingCategory.name} />
					</div>
					<div>
						<Label for="budgeted_amount">Budgeted Amount</Label>
						<Input
							id="budgeted_amount"
							type="number"
							placeholder="Enter budgeted amount"
							bind:value={editingCategory.budgeted_amount}
						/>
					</div>
					<div>
						<Label for="color_code">Color Code</Label>
						<Input
							id="color_code"
							type="text"
							placeholder="Enter color code"
							bind:value={editingCategory.color_code}
						/>
					</div>
					<div>
						<Label for="description">Description</Label>
						<Input
							id="description"
							type="text"
							placeholder="Enter description"
							bind:value={editingCategory.description}
						/>
					</div>
				</form>
			</Card.Content>
			<Card.Footer class="flex justify-end space-x-2">
				<Button variant="outline" on:click={() => (showEditModalState = false)}>Cancel</Button>
				<Button on:click={handleEditSubmit}>Update</Button>
			</Card.Footer>
		</Card.Root>
	</div>
{/if}

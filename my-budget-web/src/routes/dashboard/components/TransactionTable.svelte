<script lang="ts">
	import type { TransactionCreateRequest, Transaction, Category } from '../../../types/types';
	import { deleteTransaction, createTransaction } from '$lib/api/transaction';
	import { toast } from 'svelte-french-toast';
	import { fetchTransactions, updateTransaction } from '$lib/api/transaction';
	import { categoriesStore } from '$lib/store';
	import { Button } from '$lib/components/ui/button';
	import * as Table from '$lib/components/ui/table';
	import * as Card from '$lib/components/ui/card/index.js';
	import { Label } from '$lib/components/ui/label';
	import { Input } from '$lib/components/ui/input';

	export let transactions: Transaction[] = [];
	// After fetching or updating transactions, sort them:
	$: transactions = transactions.sort(
		(a, b) => new Date(b.CreatedAt).getTime() - new Date(a.CreatedAt).getTime()
	);

	let categories: Category[] = [];

	categoriesStore.subscribe(($categories: Category[]) => {
		categories = $categories;
	});

	function findCategoryName(categoryId: number): string {
		const category = categories.find((c) => c.id === categoryId);
		return category ? category.name : 'Unknown';
	}

	let showCreateModal = false; // This controls the visibility of the create transaction modal

	// Example formatting functions, adjust as needed
	function formatDate(dateString: string) {
		return new Intl.DateTimeFormat('en-US', { dateStyle: 'medium' }).format(new Date(dateString));
	}

	function formatAmount(amount: number) {
		return new Intl.NumberFormat('en-US', { style: 'currency', currency: 'USD' }).format(amount);
	}

	let isModalOpen = false;
	let selectedTransaction: Transaction | null = null;

	function showModal(transaction: Transaction) {
		selectedTransaction = transaction;
		isModalOpen = true;
	}

	let showEditModalState = false;
	let editingTransaction: Transaction | null = null;

	function showEditModal(transaction: Transaction) {
		editingTransaction = transaction;
		showEditModalState = true;
	}

	function closeModal() {
		isModalOpen = false;
		showCreateModal = false; // Add this line to close the create transaction modal
	}

	async function handleDelete() {
		if (!selectedTransaction) return;

		try {
			const token = localStorage.getItem('access_token');
			if (!token) {
				toast.error("You're not authenticated.");
				return;
			}
			await deleteTransaction(
				import.meta.env.VITE_API_URL,
				token,
				selectedTransaction.TransactionID
			);
			toast.success('Transaction deleted successfully.');

			// Optionally, refresh the transactions list here
			// For example:
			// transactions = transactions.filter(t => t.TransactionID !== selectedTransaction.TransactionID);

			closeModal();
		} catch (error) {
			console.error('Failed to delete the transaction:', error);
			toast.error('Failed to delete the transaction.');
		}
	}

	let transactionForm: TransactionCreateRequest = {
		Amount: 0,
		Date: '',
		Description: '',
		Note: '',
		Location: '',
		CategoryID: 0,
		Is_Income: false
	};

	async function handleSubmit() {
		const token = localStorage.getItem('access_token'); // Ensure secure handling
		if (!token) {
			toast.error('You must be logged in to perform this action.');
			return;
		}

		try {
			await createTransaction(import.meta.env.VITE_API_URL, token, transactionForm);
			toast.success('Transaction created successfully.');
			await fetchTransactions(import.meta.env.VITE_API_URL, token); // Refresh the transactions list
			const updatedTransactions = await fetchTransactions(import.meta.env.VITE_API_URL, token); // Fetch updated list
			transactions = updatedTransactions; // Update the transactions array in the component
			showCreateModal = false; // Close the modal
			// Clear form, update UI, navigate, or refresh data as necessary
		} catch (error) {
			toast.error('Failed to create transaction.');
			console.error(error);
		}
	}

	// Define the handleEditSubmit function here
	async function handleEditSubmit() {
		if (!editingTransaction) return;

		const token = localStorage.getItem('access_token');
		if (!token) {
			toast.error('You must be logged in to perform this action.');
			return;
		}

		try {
			// Assume updateTransaction function exists and sends a PATCH/PUT request to update the transaction
			await updateTransaction(
				import.meta.env.VITE_API_URL,
				token,
				editingTransaction.TransactionID,
				{
					// Payload with the transaction data to update
					Amount: editingTransaction.Amount,
					Date: editingTransaction.Date,
					Description: editingTransaction.Description,
					Note: editingTransaction.Note,
					Location: editingTransaction.Location,
					CategoryID: editingTransaction.CategoryID,
					Is_Income: editingTransaction.Is_Income
				}
			);
			toast.success('Transaction updated successfully.');
			showEditModalState = false;
			// Refresh your transactions list to show the updated data
			fetchTransactions(import.meta.env.VITE_API_URL, token).then((updatedTransactions) => {
				transactions = updatedTransactions;
			});
		} catch (error) {
			toast.error('Failed to update transaction.');
			console.error(error);
		}
	}
</script>

<div class="flex justify-between items-center mb-4">
	<div class="text-xl font-semibold">Transactions</div>
	<Button variant="default" on:click={() => (showCreateModal = true)}>+ Create Transaction</Button>
</div>

<Table.Root>
	<Table.Caption>Transactions</Table.Caption>
	<Table.Header>
		<Table.Row>
			<Table.Head class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider"
				>Date</Table.Head
			>
			<Table.Head class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider"
				>Description</Table.Head
			>
			<Table.Head class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider"
				>Amount ($)</Table.Head
			>
			<Table.Head class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider"
				>Type</Table.Head
			>
			<Table.Head class="px-6 py-3 text-left text-xs font-medium uppercase tracking-wider"
				>Category</Table.Head
			>
			<Table.Head class="relative px-6 py-3"><span class="sr-only">View More</span></Table.Head>
		</Table.Row>
	</Table.Header>
	<Table.Body>
		{#each transactions as transaction (transaction.TransactionID)}
			<Table.Row>
				<Table.Cell class="px-6 py-4 whitespace-nowrap">{transaction.Date}</Table.Cell>
				<Table.Cell class="px-6 py-4 whitespace-nowrap">{transaction.Description}</Table.Cell>
				<Table.Cell class="px-6 py-4 whitespace-nowrap">$ {transaction.Amount}</Table.Cell>
				<Table.Cell class="px-6 py-4 whitespace-nowrap"
					>{transaction.Is_Income ? 'Income' : 'Expense'}</Table.Cell
				>
				<Table.Cell class="px-6 py-4 whitespace-nowrap"
					>{findCategoryName(transaction.CategoryID)}</Table.Cell
				>
				<Table.Cell class="px-6 py-4 whitespace-nowrap text-right text-sm font-medium">
					<Button variant="secondary" on:click={() => showModal(transaction)}>View More</Button>
					<Button variant="outline" on:click={() => showEditModal(transaction)}>Edit</Button>
				</Table.Cell>
			</Table.Row>
		{/each}
	</Table.Body>
</Table.Root>

{#if isModalOpen}
	<div class="fixed inset-0 z-50 overflow-y-auto flex justify-center items-center">
		<button
			class="fixed inset-0 bg-black bg-opacity-50"
			on:click={closeModal}
			type="button"
			aria-label="Close Modal"
		></button>
		<Card.Root
			class="w-full max-w-lg m-4 rounded-lg overflow-hidden shadow-2xl transform transition-all"
		>
			<Card.Header>
				<Card.Title>Transaction Details</Card.Title>
			</Card.Header>
			<Card.Content>
				<div class="space-y-4">
					<div>
						<Label>Date</Label>
						<Input
							disabled
							value={selectedTransaction ? formatDate(selectedTransaction.Date) : ''}
						/>
					</div>
					<div>
						<Label>Description</Label>
						<Input disabled value={selectedTransaction ? selectedTransaction.Description : ''} />
					</div>
					<div>
						<Label>Location</Label>
						<Input disabled value={selectedTransaction ? selectedTransaction.Location : ''} />
					</div>
					<div>
						<Label>Amount</Label>
						<Input
							disabled
							value={selectedTransaction ? formatAmount(selectedTransaction.Amount) : ''}
						/>
					</div>
					<div>
						<Label>Type</Label>
						<Input
							disabled
							value={selectedTransaction
								? selectedTransaction.Is_Income
									? 'Income'
									: 'Expense'
								: ''}
						/>
					</div>
					<div>
						<Label>Notes</Label>
						<Input disabled value={selectedTransaction ? selectedTransaction.Note : ''} />
					</div>

					<!-- Add more details as necessary -->
				</div>
			</Card.Content>
			<Card.Footer class="flex justify-end space-x-2">
				<Button variant="outline" on:click={closeModal}>Close</Button>
				<Button variant="destructive" on:click={handleDelete}>Delete</Button>
			</Card.Footer>
		</Card.Root>
	</div>
{/if}
{#if showCreateModal}
	<div class="fixed inset-0 z-50 overflow-y-auto flex justify-center items-center">
		<button
			class="fixed inset-0 bg-black bg-opacity-50"
			on:click={closeModal}
			type="button"
			aria-label="Close modal"
		></button>
		<!-- Background overlay -->
		<Card.Root
			class="w-full max-w-lg m-4  rounded-lg overflow-hidden shadow-2xl transform transition-all"
		>
			<Card.Header>
				<Card.Title>Create New Transaction</Card.Title>
			</Card.Header>
			<Card.Content>
				<form on:submit|preventDefault={handleSubmit}>
					<!-- Form fields -->
					<div class="space-y-4">
						<!-- Similar structure for each field as before, adjusted for your content -->
						<label for="date" class="block text-sm font-bold">Date</label>
						<input
							class="w-full p-2 border rounded"
							type="date"
							id="date"
							bind:value={transactionForm.Date}
							required
						/>

						<label for="description" class="block text-sm font-bold">Description</label>
						<input
							class="w-full p-2 border rounded"
							type="text"
							id="description"
							bind:value={transactionForm.Description}
							placeholder="Transaction Description"
							required
						/>

						<label for="amount" class="block text-sm font-bold">Amount</label>
						<input
							class="w-full p-2 border rounded"
							type="number"
							step="0.01"
							id="amount"
							bind:value={transactionForm.Amount}
							placeholder="0.00"
							required
						/>
						<div>
							<label class="flex items-center">
								<input type="checkbox" bind:checked={transactionForm.Is_Income} />
								<span class="ml-2">Is Income?</span>
							</label>
						</div>
						<!-- Add more fields as necessary -->
						<Card.Footer class="flex flex-col space-y-2">
							<Button type="submit" class="w-full">Create Transaction</Button>
							<Button variant="destructive" on:click={closeModal} class="w-full">Cancel</Button>
						</Card.Footer>
					</div>
					<!-- End of Form Fields -->
				</form></Card.Content
			>
		</Card.Root>
	</div>
{/if}
{#if showEditModalState && editingTransaction}
	<div class="fixed inset-0 z-50 overflow-y-auto flex justify-center items-center">
		<button
			class="fixed inset-0 bg-black bg-opacity-50"
			on:click={() => (showEditModalState = false)}
			type="button"
			aria-label="Close edit modal"
		></button>
		<!-- Modal Content -->
		<Card.Root
			class="w-full max-w-lg m-4 rounded-lg overflow-hidden shadow-2xl transform transition-all"
		>
			<Card.Header>
				<Card.Title>Edit Transaction</Card.Title>
			</Card.Header>
			<Card.Content>
				<form on:submit|preventDefault={handleEditSubmit}>
					<div class="space-y-4">
						<div>
							<Label for="edit-date">Date</Label>
							<Input id="edit-date" type="date" bind:value={editingTransaction.Date} />
						</div>
						<div>
							<Label for="edit-description">Description</Label>
							<Input
								id="edit-description"
								type="text"
								bind:value={editingTransaction.Description}
							/>
						</div>
						<div>
							<Label for="edit-notes">Note</Label>
							<Input id="edit-notes" type="text" bind:value={editingTransaction.Note} />
						</div>
						<div>
							<Label for="edit-location">Location</Label>
							<Input id="edit-location" type="text" bind:value={editingTransaction.Location} />
						</div>
						<div>
							<Label for="edit-amount">Amount</Label>
							<Input
								id="edit-amount"
								type="number"
								step="0.01"
								bind:value={editingTransaction.Amount}
							/>
						</div>
						<div>
							<Label for="edit-type">Type</Label>
							<select bind:value={editingTransaction.Is_Income} class="w-full p-2 border rounded">
								<option value={true}>Income</option>
								<option value={false}>Expense</option>
							</select>
						</div>
						<div>
							<Label for="edit-category">Category</Label>
							<select bind:value={editingTransaction.CategoryID} class="w-full p-2 border rounded">
								{#each categories as category}
									<option value={category.id}>{category.name}</option>
								{/each}
							</select>
						</div>
					</div>
					<Card.Footer class="flex justify-end space-x-2 mt-4">
						<Button variant="outline" on:click={() => (showEditModalState = false)}>Cancel</Button>
						<Button type="submit">Save Changes</Button>
					</Card.Footer>
				</form>
			</Card.Content>
		</Card.Root>
	</div>
{/if}

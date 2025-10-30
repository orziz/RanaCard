import { defineStore } from 'pinia'

export interface CardRoot { Name: string; Cards: any[] }
export interface PendantRoot { Name: string; Pendant: any[] }

export const useDataStore = defineStore('data', {
  state: () => ({
    cards: null as CardRoot | null,
    pendants: null as PendantRoot | null
  }),
  actions: {
    setCards(data: CardRoot) { this.cards = data },
    setPendants(data: PendantRoot) { this.pendants = data },
    exportBlob(kind: 'card' | 'pendant') {
      const data = kind === 'card' ? this.cards : this.pendants
      if (!data) return null
      const text = JSON.stringify(data, null, 2)
      return new Blob([text], { type: 'application/json;charset=utf-8' })
    }
  }
})


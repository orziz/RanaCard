import { defineStore } from 'pinia'

export interface CardRoot { Name: string; Cards: any[] }
export interface PendantRoot { Name: string; Pendant: any[] }
export type MapEvent = {
  ID: string
  Name: string
  LimitStage?: number
  Character?: string
  Content?: string
  Choices?: Array<{ Description?: string; Effect?: string }>
}

export type BeginEffect = {
  ID: string
  EffectDescription?: string
  EffectString?: string
  UnLocked?: number
  UnlockCondition?: string
  StarCount?: number
}

export const useDataStore = defineStore('data', {
  state: () => ({
    cards: null as CardRoot | null,
    pendants: null as PendantRoot | null,
    mapEvents: null as MapEvent[] | null,
    beginEffects: null as BeginEffect[] | null
  }),
  actions: {
    setCards(data: CardRoot) { this.cards = data },
    setPendants(data: PendantRoot) { this.pendants = data },
    setMapEvents(list: MapEvent[]) { this.mapEvents = list },
    setBeginEffects(list: BeginEffect[]) { this.beginEffects = list },
    exportBlob(kind: 'card' | 'pendant') {
      const data = kind === 'card' ? this.cards : this.pendants
      if (!data) return null
      const text = JSON.stringify(data, null, 2)
      return new Blob([text], { type: 'application/json;charset=utf-8' })
    }
  }
})

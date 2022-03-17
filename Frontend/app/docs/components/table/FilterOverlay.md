# FilterOverlay

## Props

| Name              | Type    | Description |
| ----------------- | ------- | ----------- |
| `current-filters` | `Array` | &nbsp;      |

## Data

| Name              | Type     | Description | Initial value         |
| ----------------- | -------- | ----------- | --------------------- |
| `newFilters`      | `object` |             | `this.currentFilters` |
| `filterAttribute` | `string` |             | `""`                  |

## Events

| Name            | Description                                                       |
| --------------- | ----------------------------------------------------------------- |
| `update-filter` | <br/>**Arguments**<br/><ul><li>**`newFilters: object`**</li></ul> |

## Methods

### removeAllFilters()

**Syntax**

```typescript
removeAllFilters(): void
```

### addFilter()

**Syntax**

```typescript
addFilter(filter: unknown): void
```

### removeFilter()

**Syntax**

```typescript
removeFilter(attribute: unknown): void
```

### findFilter()

**Syntax**

```typescript
findFilter(attribute: unknown): unknown
```


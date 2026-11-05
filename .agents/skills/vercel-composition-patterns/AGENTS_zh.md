# React 组合模式

**Version 1.0.0**  
Engineering  
January 2026

> **注意：**  
> 本文档主要供智能体与 LLM 在维护、  
> 生成或重构采用组合模式的 React 代码库时遵循。人类读者  
> 也可参考，但此处指导针对 AI 辅助工作流的自动化  
> 与一致性做了优化。

---

## 摘要

用于构建灵活、可维护 React 组件的组合模式。通过复合组件、状态提升与内部组合来避免布尔 prop 泛滥。这些模式使代码库在规模扩大时更便于人类与 AI 智能体协作。

---

## 目录

1. [组件架构](#1-component-architecture) — **高**
   - 1.1 [避免布尔 Prop 泛滥](#11-avoid-boolean-prop-proliferation)
   - 1.2 [使用复合组件](#12-use-compound-components)
2. [状态管理](#2-state-management) — **中**
   - 2.1 [将状态管理与 UI 解耦](#21-decouple-state-management-from-ui)
   - 2.2 [为依赖注入定义通用 Context 接口](#22-define-generic-context-interfaces-for-dependency-injection)
   - 2.3 [将状态提升到 Provider 组件](#23-lift-state-into-provider-components)
3. [实现模式](#3-implementation-patterns) — **中**
   - 3.1 [创建显式组件变体](#31-create-explicit-component-variants)
   - 3.2 [优先用 children 组合而非 Render Props](#32-prefer-composing-children-over-render-props)
4. [React 19 API](#4-react-19-apis) — **中**
   - 4.1 [React 19 API 变更](#41-react-19-api-changes)

---

## 1. 组件架构

**影响：高**

用于组织组件结构、避免 prop 泛滥并支持灵活组合的基础模式。

### 1.1 避免布尔 Prop 泛滥

**影响：关键（避免不可维护的组件变体）**

不要用 `isThread`、`isEditing`、`isDMThread` 等布尔 prop 来定制

组件行为。每增加一个布尔 prop，可能状态数就翻倍，并产生

难以维护的条件逻辑。请改用组合。

**错误：布尔 prop 带来指数级复杂度**

```tsx
function Composer({
  onSubmit,
  isThread,
  channelId,
  isDMThread,
  dmId,
  isEditing,
  isForwarding,
}: Props) {
  return (
    <form>
      <Header />
      <Input />
      {isDMThread ? (
        <AlsoSendToDMField id={dmId} />
      ) : isThread ? (
        <AlsoSendToChannelField id={channelId} />
      ) : null}
      {isEditing ? (
        <EditActions />
      ) : isForwarding ? (
        <ForwardActions />
      ) : (
        <DefaultActions />
      )}
      <Footer onSubmit={onSubmit} />
    </form>
  )
}
```

**正确：组合消除条件分支**

```tsx
// Channel composer
function ChannelComposer() {
  return (
    <Composer.Frame>
      <Composer.Header />
      <Composer.Input />
      <Composer.Footer>
        <Composer.Attachments />
        <Composer.Formatting />
        <Composer.Emojis />
        <Composer.Submit />
      </Composer.Footer>
    </Composer.Frame>
  )
}

// Thread composer - adds "also send to channel" field
function ThreadComposer({ channelId }: { channelId: string }) {
  return (
    <Composer.Frame>
      <Composer.Header />
      <Composer.Input />
      <AlsoSendToChannelField id={channelId} />
      <Composer.Footer>
        <Composer.Formatting />
        <Composer.Emojis />
        <Composer.Submit />
      </Composer.Footer>
    </Composer.Frame>
  )
}

// Edit composer - different footer actions
function EditComposer() {
  return (
    <Composer.Frame>
      <Composer.Input />
      <Composer.Footer>
        <Composer.Formatting />
        <Composer.Emojis />
        <Composer.CancelEdit />
        <Composer.SaveEdit />
      </Composer.Footer>
    </Composer.Frame>
  )
}
```

每种变体都明确说明渲染内容。可以共享内部实现，而无需

共用一个庞大的单体父组件。

### 1.2 使用复合组件

**影响：高（在不 prop drilling 的前提下实现灵活组合）**

将复杂组件结构化为带共享 context 的复合组件。各

子组件通过 context 访问共享状态，而非 props。使用者按需组合

所需片段。

**错误：带 render props 的单体组件**

```tsx
function Composer({
  renderHeader,
  renderFooter,
  renderActions,
  showAttachments,
  showFormatting,
  showEmojis,
}: Props) {
  return (
    <form>
      {renderHeader?.()}
      <Input />
      {showAttachments && <Attachments />}
      {renderFooter ? (
        renderFooter()
      ) : (
        <Footer>
          {showFormatting && <Formatting />}
          {showEmojis && <Emojis />}
          {renderActions?.()}
        </Footer>
      )}
    </form>
  )
}
```

**正确：带共享 context 的复合组件**

```tsx
const ComposerContext = createContext<ComposerContextValue | null>(null)

function ComposerProvider({ children, state, actions, meta }: ProviderProps) {
  return (
    <ComposerContext value={{ state, actions, meta }}>
      {children}
    </ComposerContext>
  )
}

function ComposerFrame({ children }: { children: React.ReactNode }) {
  return <form>{children}</form>
}

function ComposerInput() {
  const {
    state,
    actions: { update },
    meta: { inputRef },
  } = use(ComposerContext)
  return (
    <TextInput
      ref={inputRef}
      value={state.input}
      onChangeText={(text) => update((s) => ({ ...s, input: text }))}
    />
  )
}

function ComposerSubmit() {
  const {
    actions: { submit },
  } = use(ComposerContext)
  return <Button onPress={submit}>Send</Button>
}

// Export as compound component
const Composer = {
  Provider: ComposerProvider,
  Frame: ComposerFrame,
  Input: ComposerInput,
  Submit: ComposerSubmit,
  Header: ComposerHeader,
  Footer: ComposerFooter,
  Attachments: ComposerAttachments,
  Formatting: ComposerFormatting,
  Emojis: ComposerEmojis,
}
```

**用法：**

```tsx
<Composer.Provider state={state} actions={actions} meta={meta}>
  <Composer.Frame>
    <Composer.Header />
    <Composer.Input />
    <Composer.Footer>
      <Composer.Formatting />
      <Composer.Submit />
    </Composer.Footer>
  </Composer.Frame>
</Composer.Provider>
```

使用者显式组合所需内容，没有隐藏的条件分支。state、actions 与 meta 由父级 Provider 注入，同一组件结构可在多种场景复用。

---

## 2. 状态管理

**影响：中**

在组合组件之间提升状态、管理共享 context 的模式。

### 2.1 将状态管理与 UI 解耦

**影响：中（在不改 UI 的情况下可替换状态实现）**

Provider 组件应是唯一知晓状态如何管理的地方。

UI 组件只消费 context 接口——它们不关心状态来自

`useState`、Zustand 还是服务端同步。

**错误：UI 与状态实现耦合**

```tsx
function ChannelComposer({ channelId }: { channelId: string }) {
  // UI component knows about global state implementation
  const state = useGlobalChannelState(channelId)
  const { submit, updateInput } = useChannelSync(channelId)

  return (
    <Composer.Frame>
      <Composer.Input
        value={state.input}
        onChange={(text) => sync.updateInput(text)}
      />
      <Composer.Submit onPress={() => sync.submit()} />
    </Composer.Frame>
  )
}
```

**正确：状态管理隔离在 Provider 内**

```tsx
// Provider handles all state management details
function ChannelProvider({
  channelId,
  children,
}: {
  channelId: string
  children: React.ReactNode
}) {
  const { state, update, submit } = useGlobalChannel(channelId)
  const inputRef = useRef(null)

  return (
    <Composer.Provider
      state={state}
      actions={{ update, submit }}
      meta={{ inputRef }}
    >
      {children}
    </Composer.Provider>
  )
}

// UI component only knows about the context interface
function ChannelComposer() {
  return (
    <Composer.Frame>
      <Composer.Header />
      <Composer.Input />
      <Composer.Footer>
        <Composer.Submit />
      </Composer.Footer>
    </Composer.Frame>
  )
}

// Usage
function Channel({ channelId }: { channelId: string }) {
  return (
    <ChannelProvider channelId={channelId}>
      <ChannelComposer />
    </ChannelProvider>
  )
}
```

**不同 Provider，相同 UI：**

```tsx
// Local state for ephemeral forms
function ForwardMessageProvider({ children }) {
  const [state, setState] = useState(initialState)
  const forwardMessage = useForwardMessage()

  return (
    <Composer.Provider
      state={state}
      actions={{ update: setState, submit: forwardMessage }}
    >
      {children}
    </Composer.Provider>
  )
}

// Global synced state for channels
function ChannelProvider({ channelId, children }) {
  const { state, update, submit } = useGlobalChannel(channelId)

  return (
    <Composer.Provider state={state} actions={{ update, submit }}>
      {children}
    </Composer.Provider>
  )
}
```

同一 `Composer.Input` 可在两种 Provider 下工作，因为它只依赖

context 接口，而非具体实现。

### 2.2 为依赖注入定义通用 Context 接口

**影响：高（跨用例实现可注入的状态）**

为组件 context 定义包含三部分的**通用接口**：

`state`、`actions` 与 `meta`。该接口是任意 Provider 均可实现的契约——

使同一套 UI 组件能配合完全不同的状态实现工作。

**核心原则：** 提升状态、组合内部结构、使状态可依赖注入。

**错误：UI 与特定状态实现耦合**

```tsx
function ComposerInput() {
  // Tightly coupled to a specific hook
  const { input, setInput } = useChannelComposerState()
  return <TextInput value={input} onChangeText={setInput} />
}
```

**正确：通用接口支持依赖注入**

```tsx
// Define a GENERIC interface that any provider can implement
interface ComposerState {
  input: string
  attachments: Attachment[]
  isSubmitting: boolean
}

interface ComposerActions {
  update: (updater: (state: ComposerState) => ComposerState) => void
  submit: () => void
}

interface ComposerMeta {
  inputRef: React.RefObject<TextInput>
}

interface ComposerContextValue {
  state: ComposerState
  actions: ComposerActions
  meta: ComposerMeta
}

const ComposerContext = createContext<ComposerContextValue | null>(null)
```

**UI 组件消费接口，而非实现：**

```tsx
function ComposerInput() {
  const {
    state,
    actions: { update },
    meta,
  } = use(ComposerContext)

  // This component works with ANY provider that implements the interface
  return (
    <TextInput
      ref={meta.inputRef}
      value={state.input}
      onChangeText={(text) => update((s) => ({ ...s, input: text }))}
    />
  )
}
```

**不同 Provider 实现同一接口：**

```tsx
// Provider A: Local state for ephemeral forms
function ForwardMessageProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState(initialState)
  const inputRef = useRef(null)
  const submit = useForwardMessage()

  return (
    <ComposerContext
      value={{
        state,
        actions: { update: setState, submit },
        meta: { inputRef },
      }}
    >
      {children}
    </ComposerContext>
  )
}

// Provider B: Global synced state for channels
function ChannelProvider({ channelId, children }: Props) {
  const { state, update, submit } = useGlobalChannel(channelId)
  const inputRef = useRef(null)

  return (
    <ComposerContext
      value={{
        state,
        actions: { update, submit },
        meta: { inputRef },
      }}
    >
      {children}
    </ComposerContext>
  )
}
```

**同一套组合 UI 在两者下均可工作：**

```tsx
// Works with ForwardMessageProvider (local state)
<ForwardMessageProvider>
  <Composer.Frame>
    <Composer.Input />
    <Composer.Submit />
  </Composer.Frame>
</ForwardMessageProvider>

// Works with ChannelProvider (global synced state)
<ChannelProvider channelId="abc">
  <Composer.Frame>
    <Composer.Input />
    <Composer.Submit />
  </Composer.Frame>
</ChannelProvider>
```

**组件外部的自定义 UI 也可访问 state 与 actions：**

```tsx
function ForwardMessageDialog() {
  return (
    <ForwardMessageProvider>
      <Dialog>
        {/* The composer UI */}
        <Composer.Frame>
          <Composer.Input placeholder="Add a message, if you'd like." />
          <Composer.Footer>
            <Composer.Formatting />
            <Composer.Emojis />
          </Composer.Footer>
        </Composer.Frame>

        {/* Custom UI OUTSIDE the composer, but INSIDE the provider */}
        <MessagePreview />

        {/* Actions at the bottom of the dialog */}
        <DialogActions>
          <CancelButton />
          <ForwardButton />
        </DialogActions>
      </Dialog>
    </ForwardMessageProvider>
  )
}

// This button lives OUTSIDE Composer.Frame but can still submit based on its context!
function ForwardButton() {
  const {
    actions: { submit },
  } = use(ComposerContext)
  return <Button onPress={submit}>Forward</Button>
}

// This preview lives OUTSIDE Composer.Frame but can read composer's state!
function MessagePreview() {
  const { state } = use(ComposerContext)
  return <Preview message={state.input} attachments={state.attachments} />
}
```

重要的是 Provider 边界，而非视觉嵌套。需要共享状态的组件

不必放在 `Composer.Frame` 内部，只需处于

Provider 范围内。

`ForwardButton` 与 `MessagePreview` 在视觉上不在编辑器

框内，但仍可访问其 state 与 actions。这正是

将状态提升到 Provider 的力量所在。

UI 是可组合的复用片段；状态由 Provider 注入。

更换 Provider，保留 UI。

### 2.3 将状态提升到 Provider 组件

**影响：高（支持在组件边界外共享状态）**

将状态管理移入专用 Provider 组件。这样主 UI 外的兄弟组件

可在无 prop drilling、无需 awkward ref 的情况下访问并修改状态。

**错误：状态困在组件内部**

```tsx
function ForwardMessageComposer() {
  const [state, setState] = useState(initialState)
  const forwardMessage = useForwardMessage()

  return (
    <Composer.Frame>
      <Composer.Input />
      <Composer.Footer />
    </Composer.Frame>
  )
}

// Problem: How does this button access composer state?
function ForwardMessageDialog() {
  return (
    <Dialog>
      <ForwardMessageComposer />
      <MessagePreview /> {/* Needs composer state */}
      <DialogActions>
        <CancelButton />
        <ForwardButton /> {/* Needs to call submit */}
      </DialogActions>
    </Dialog>
  )
}
```

**错误：用 useEffect 向上同步状态**

```tsx
function ForwardMessageDialog() {
  const [input, setInput] = useState('')
  return (
    <Dialog>
      <ForwardMessageComposer onInputChange={setInput} />
      <MessagePreview input={input} />
    </Dialog>
  )
}

function ForwardMessageComposer({ onInputChange }) {
  const [state, setState] = useState(initialState)
  useEffect(() => {
    onInputChange(state.input) // Sync on every change 😬
  }, [state.input])
}
```

**错误：提交时从 ref 读取状态**

```tsx
function ForwardMessageDialog() {
  const stateRef = useRef(null)
  return (
    <Dialog>
      <ForwardMessageComposer stateRef={stateRef} />
      <ForwardButton onPress={() => submit(stateRef.current)} />
    </Dialog>
  )
}
```

**正确：状态提升到 Provider**

```tsx
function ForwardMessageProvider({ children }: { children: React.ReactNode }) {
  const [state, setState] = useState(initialState)
  const forwardMessage = useForwardMessage()
  const inputRef = useRef(null)

  return (
    <Composer.Provider
      state={state}
      actions={{ update: setState, submit: forwardMessage }}
      meta={{ inputRef }}
    >
      {children}
    </Composer.Provider>
  )
}

function ForwardMessageDialog() {
  return (
    <ForwardMessageProvider>
      <Dialog>
        <ForwardMessageComposer />
        <MessagePreview /> {/* Custom components can access state and actions */}
        <DialogActions>
          <CancelButton />
          <ForwardButton /> {/* Custom components can access state and actions */}
        </DialogActions>
      </Dialog>
    </ForwardMessageProvider>
  )
}

function ForwardButton() {
  const { actions } = use(Composer.Context)
  return <Button onPress={actions.submit}>Forward</Button>
}
```

`ForwardButton` 位于 `Composer.Frame` 之外，但因处于 Provider 内仍可访问

submit。即便是一次性

组件，也能在 UI 结构之外访问编辑器的 state 与 actions。

**要点：** 需要共享状态的组件不必在视觉上

彼此嵌套——只需处于同一 Provider 内。

---

## 3. 实现模式

**影响：中**

实现复合组件与 context Provider 的具体技巧。

### 3.1 创建显式组件变体

**影响：中（代码自解释、无隐藏条件）**

不要用带大量布尔 prop 的单一组件，而是创建显式变体

组件。每种变体组合所需片段，代码即文档。

**错误：一个组件、多种模式**

```tsx
// What does this component actually render?
<Composer
  isThread
  isEditing={false}
  channelId='abc'
  showAttachments
  showFormatting={false}
/>
```

**正确：显式变体**

```tsx
// Immediately clear what this renders
<ThreadComposer channelId="abc" />

// Or
<EditMessageComposer messageId="xyz" />

// Or
<ForwardMessageComposer messageId="123" />
```

每种实现独特、显式且自包含，同时可共用

部分内部模块。

**实现示例：**

```tsx
function ThreadComposer({ channelId }: { channelId: string }) {
  return (
    <ThreadProvider channelId={channelId}>
      <Composer.Frame>
        <Composer.Input />
        <AlsoSendToChannelField channelId={channelId} />
        <Composer.Footer>
          <Composer.Formatting />
          <Composer.Emojis />
          <Composer.Submit />
        </Composer.Footer>
      </Composer.Frame>
    </ThreadProvider>
  )
}

function EditMessageComposer({ messageId }: { messageId: string }) {
  return (
    <EditMessageProvider messageId={messageId}>
      <Composer.Frame>
        <Composer.Input />
        <Composer.Footer>
          <Composer.Formatting />
          <Composer.Emojis />
          <Composer.CancelEdit />
          <Composer.SaveEdit />
        </Composer.Footer>
      </Composer.Frame>
    </EditMessageProvider>
  )
}

function ForwardMessageComposer({ messageId }: { messageId: string }) {
  return (
    <ForwardMessageProvider messageId={messageId}>
      <Composer.Frame>
        <Composer.Input placeholder="Add a message, if you'd like." />
        <Composer.Footer>
          <Composer.Formatting />
          <Composer.Emojis />
          <Composer.Mentions />
        </Composer.Footer>
      </Composer.Frame>
    </ForwardMessageProvider>
  )
}
```

每种变体明确说明：

- 使用的 Provider / 状态

- 包含的 UI 元素

- 可用的操作

无需推演布尔 prop 组合，也不存在不可能的状态。

### 3.2 优先用 children 组合而非 Render Props

**影响：中（组合更清晰、可读性更好）**

用 `children` 做组合，而非 `renderX` props。children 更易读、

组合更自然，也无需理解回调

签名。

**错误：render props**

```tsx
function Composer({
  renderHeader,
  renderFooter,
  renderActions,
}: {
  renderHeader?: () => React.ReactNode
  renderFooter?: () => React.ReactNode
  renderActions?: () => React.ReactNode
}) {
  return (
    <form>
      {renderHeader?.()}
      <Input />
      {renderFooter ? renderFooter() : <DefaultFooter />}
      {renderActions?.()}
    </form>
  )
}

// Usage is awkward and inflexible
return (
  <Composer
    renderHeader={() => <CustomHeader />}
    renderFooter={() => (
      <>
        <Formatting />
        <Emojis />
      </>
    )}
    renderActions={() => <SubmitButton />}
  />
)
```

**正确：带 children 的复合组件**

```tsx
function ComposerFrame({ children }: { children: React.ReactNode }) {
  return <form>{children}</form>
}

function ComposerFooter({ children }: { children: React.ReactNode }) {
  return <footer className='flex'>{children}</footer>
}

// Usage is flexible
return (
  <Composer.Frame>
    <CustomHeader />
    <Composer.Input />
    <Composer.Footer>
      <Composer.Formatting />
      <Composer.Emojis />
      <SubmitButton />
    </Composer.Footer>
  </Composer.Frame>
)
```

**适合使用 render props 的场景：**

```tsx
// Render props work well when you need to pass data back
<List
  data={items}
  renderItem={({ item, index }) => <Item item={item} index={index} />}
/>
```

当父组件需要向子组件提供数据或状态时，使用 render props。

组合静态结构时，使用 children。

---

## 4. React 19 API

**影响：中**

仅适用于 React 19+。不要使用 `forwardRef`；用 `use()` 替代 `useContext()`。

### 4.1 React 19 API 变更

**影响：中（组件定义与 context 用法更简洁）**

> **⚠️ 仅 React 19+。** 若使用 React 18 或更早版本，可跳过本节。

在 React 19 中，`ref` 为普通 prop（无需 `forwardRef` 包装），且 `use()` 取代 `useContext()`。

**错误：React 19 中仍使用 forwardRef**

```tsx
const ComposerInput = forwardRef<TextInput, Props>((props, ref) => {
  return <TextInput ref={ref} {...props} />
})
```

**正确：ref 作为普通 prop**

```tsx
function ComposerInput({ ref, ...props }: Props & { ref?: React.Ref<TextInput> }) {
  return <TextInput ref={ref} {...props} />
}
```

**错误：React 19 中仍使用 useContext**

```tsx
const value = useContext(MyContext)
```

**正确：用 use 替代 useContext**

```tsx
const value = use(MyContext)
```

与 `useContext()` 不同，`use()` 也可在条件分支中调用。

---

## 参考资料

1. [https://react.dev](https://react.dev)
2. [https://react.dev/learn/passing-data-deeply-with-context](https://react.dev/learn/passing-data-deeply-with-context)
3. [https://react.dev/reference/react/use](https://react.dev/reference/react/use)

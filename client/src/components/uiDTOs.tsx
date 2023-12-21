export type RenderItemFunction<T> = (item: T) => JSX.Element;
export interface GenericGridProps<T> {
  items: T[];
  renderItem: RenderItemFunction<T>;
}

# pipelines.py

from itemadapter import ItemAdapter
from rich.console import Console
from rich.text import Text

console = Console()


class RichLoggingPipeline:
    def open_spider(self, spider):
        console.log(f"[bold green]Spider {spider.name} opened")

    def close_spider(self, spider):
        console.log(f"[bold red]Spider {spider.name} closed")

    def process_item(self, item, spider):
        adapter = ItemAdapter(item)
        for field_name in adapter.field_names():
            field_value = adapter.get(field_name)
            console.print(
                f"[bold cyan]{field_name}[/bold cyan]: [yellow]{field_value}[/yellow]")

        return item

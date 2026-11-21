"""Render actual notebook plots and Parquet rows for the English report."""
import base64
import json
from pathlib import Path
import shutil
import pandas as pd
import matplotlib
matplotlib.use('Agg')
import matplotlib.pyplot as plt

ROOT=Path(__file__).resolve().parents[2]
REPORT=ROOT/'workshop_3/report'


def main():
    assets=REPORT/'assets';assets.mkdir(parents=True,exist_ok=True)
    shutil.copyfile(ROOT/'workshop_2/report/assets/Escudo.png',assets/'Escudo.png')
    notebook=json.loads((ROOT/'notebooks/03_silver_quality_review.ipynb').read_text())
    index=0
    for cell in notebook['cells']:
        for output in cell.get('outputs',[]):
            encoded=output.get('data',{}).get('image/png')
            if encoded:
                index+=1
                (assets/f'quality_{index}.png').write_bytes(base64.b64decode(encoded))
    register=json.loads((ROOT/'workshop_3/evidence/guide_gold_samples.json').read_text())
    for kind in ('governance','storytelling'):
        path=ROOT/register['outputs'][kind]['path']
        data=pd.read_parquet(path)
        if kind=='governance':
            preview=data[(data['source']=='ghcn_daily') & (data['metric']=='monthly_records')].head(5)[['source','period','metric','value']]
        else:
            preview=data.head(5)[['period','event_type','severity_unit','record_count','mean_value','precipitation_total_mm']]
        preview.to_csv(ROOT/f'workshop_3/samples/gold/{kind}_preview.csv',index=False)
        shown=preview.astype(object).fillna('null')
        for col in shown:
            shown[col]=shown[col].map(lambda x:f'{x:.4f}' if isinstance(x,float) else str(x))
        shown.columns=[c.replace('_','\n') for c in shown.columns]
        fig,ax=plt.subplots(figsize=(11,2.5));ax.axis('off')
        table=ax.table(cellText=shown.values,colLabels=shown.columns,cellLoc='center',loc='center')
        table.auto_set_font_size(False);table.set_fontsize(9);table.scale(1,1.9)
        for (r,c),cell in table.get_celld().items():
            if r==0:cell.set_facecolor('#1F4E79');cell.set_text_props(color='white',weight='bold');cell.set_height(0.28)
            elif r%2:cell.set_facecolor('#EAF2F8')
            cell.set_edgecolor('#CCD6DD')
        ax.set_title(f'{kind.title()}: rendered preview of actual Spark Parquet ({len(data):,} rows)',fontsize=12,pad=8)
        fig.tight_layout();fig.savefig(assets/(kind+'_preview.png'),dpi=180,bbox_inches='tight');plt.close(fig)
    story=pd.read_parquet(ROOT/register['outputs']['storytelling']['path'])
    text=story[story.text_record_count.gt(0)]
    preview=text[['period','event_type','text_record_count','mean_sentiment_score',
                  'positive_count','neutral_count','negative_count']].head(6)
    preview.to_csv(ROOT/'workshop_3/samples/gold/text_preview.csv',index=False)
    shown=preview.astype(object).fillna('null')
    for col in shown:
        shown[col]=shown[col].map(lambda x:f'{x:.3f}' if isinstance(x,float) else str(x))
    shown.columns=[c.replace('_','\n') for c in shown.columns]
    fig,ax=plt.subplots(figsize=(11,2.7));ax.axis('off')
    table=ax.table(cellText=shown.values,colLabels=shown.columns,cellLoc='center',loc='center')
    table.auto_set_font_size(False);table.set_fontsize(8);table.scale(1,1.7)
    for (r,c),cell in table.get_celld().items():
        if r==0:cell.set_facecolor('#1F4E79');cell.set_text_props(color='white',weight='bold')
        elif r%2:cell.set_facecolor('#EAF2F8')
        cell.set_edgecolor('#CCD6DD')
    ax.set_title('2021 NOAA narrative columns from verified Gold Parquet',fontsize=12,pad=8)
    fig.tight_layout();fig.savefig(assets/'text_preview.png',dpi=180,bbox_inches='tight');plt.close(fig)
    print('Saved notebook figures and exact Parquet-derived previews.')


if __name__=='__main__':main()
